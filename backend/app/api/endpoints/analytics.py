from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta
from typing import Optional
from app.db.session import get_db
from app.schemas.analytics import AnalyticsEventCreate, AnalyticsEventResponse, AnalyticsSummary
from app.models.analytics import AnalyticsEvent
from app.models.contact import ContactSubmission
from app.api.deps import get_current_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/event", response_model=dict, status_code=201)
async def track_event(
    event: AnalyticsEventCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Track an analytics event.
    Public endpoint - no authentication required.
    """
    try:
        # Get client info
        client_host = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        referrer = request.headers.get("referer")
        
        # Create event
        analytics_event = AnalyticsEvent(
            event_type=event.event_type,
            event_data=event.event_data,
            session_id=event.session_id,
            ip_address=client_host,
            user_agent=user_agent,
            referrer=referrer or event.referrer
        )
        
        db.add(analytics_event)
        db.commit()
        
        return {"success": True, "message": "Event tracked"}
        
    except Exception as e:
        logger.error(f"Analytics tracking failed: {str(e)}")
        db.rollback()
        # Don't fail the request - analytics should be silent
        return {"success": False, "message": "Event tracking failed"}


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """
    Get analytics summary (admin only).
    """
    # Default to last 30 days if no dates provided
    if not end_date:
        end_date = date.today()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Convert dates to datetime for queries
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    # Total events in date range
    total_events = db.query(func.count(AnalyticsEvent.id)).filter(
        AnalyticsEvent.timestamp >= start_datetime,
        AnalyticsEvent.timestamp <= end_datetime
    ).scalar()
    
    # Total submissions in date range
    total_submissions = db.query(func.count(ContactSubmission.id)).filter(
        ContactSubmission.submitted_at >= start_datetime,
        ContactSubmission.submitted_at <= end_datetime
    ).scalar()
    
    # Unique sessions
    unique_sessions = db.query(
        func.count(func.distinct(AnalyticsEvent.session_id))
    ).filter(
        AnalyticsEvent.timestamp >= start_datetime,
        AnalyticsEvent.timestamp <= end_datetime,
        AnalyticsEvent.session_id.isnot(None)
    ).scalar()
    
    # Top events
    top_events_query = db.query(
        AnalyticsEvent.event_type,
        func.count(AnalyticsEvent.id).label('count')
    ).filter(
        AnalyticsEvent.timestamp >= start_datetime,
        AnalyticsEvent.timestamp <= end_datetime
    ).group_by(
        AnalyticsEvent.event_type
    ).order_by(
        func.count(AnalyticsEvent.id).desc()
    ).limit(10).all()
    
    top_events = [
        {"event_type": event_type, "count": count}
        for event_type, count in top_events_query
    ]
    
    # Submissions by status
    submissions_by_status_query = db.query(
        ContactSubmission.status,
        func.count(ContactSubmission.id).label('count')
    ).filter(
        ContactSubmission.submitted_at >= start_datetime,
        ContactSubmission.submitted_at <= end_datetime
    ).group_by(
        ContactSubmission.status
    ).all()
    
    submissions_by_status = {
        status.value: count
        for status, count in submissions_by_status_query
    }
    
    return AnalyticsSummary(
        total_events=total_events or 0,
        total_submissions=total_submissions or 0,
        unique_sessions=unique_sessions or 0,
        date_range={"start": start_date, "end": end_date},
        top_events=top_events,
        submissions_by_status=submissions_by_status
    )
