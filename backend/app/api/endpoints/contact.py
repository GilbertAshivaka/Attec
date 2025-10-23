from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.schemas.contact import (
    ContactSubmissionCreate,
    ContactSubmissionResponse,
    ContactSubmissionUpdate,
    ContactSubmissionList
)
from app.models.contact import ContactSubmission, ContactStatus
from app.services.email_service import email_service
from app.api.deps import get_current_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_contact_submission(
    contact: ContactSubmissionCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Submit a contact form.
    Public endpoint - no authentication required.
    """
    try:
        # Get client info
        client_host = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Create submission
        submission = ContactSubmission(
            name=contact.name,
            email=contact.email,
            company=contact.company,
            message=contact.message,
            ip_address=client_host,
            user_agent=user_agent
        )
        
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        # Send emails asynchronously (don't block the response)
        try:
            await email_service.send_lead_notification(
                contact_name=contact.name,
                contact_email=contact.email,
                contact_company=contact.company or "Not provided",
                contact_message=contact.message,
                submission_id=str(submission.id)
            )
            
            await email_service.send_auto_reply(
                contact_name=contact.name,
                contact_email=contact.email
            )
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            # Don't fail the request if email fails
        
        return {
            "success": True,
            "message": "Thank you for your message. We'll be in touch within 24 hours!",
            "submission_id": str(submission.id)
        }
        
    except Exception as e:
        logger.error(f"Contact submission failed: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit contact form. Please try again."
        )


@router.get("/submissions", response_model=ContactSubmissionList)
def get_contact_submissions(
    skip: int = 0,
    limit: int = 50,
    status_filter: Optional[ContactStatus] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """
    Get all contact submissions (admin only).
    """
    query = db.query(ContactSubmission)
    
    if status_filter:
        query = query.filter(ContactSubmission.status == status_filter)
    
    total = query.count()
    submissions = query.order_by(
        ContactSubmission.submitted_at.desc()
    ).offset(skip).limit(limit).all()
    
    return ContactSubmissionList(
        total=total,
        items=submissions,
        skip=skip,
        limit=limit
    )


@router.get("/submissions/{submission_id}", response_model=ContactSubmissionResponse)
def get_contact_submission(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """
    Get a specific contact submission (admin only).
    """
    submission = db.query(ContactSubmission).filter(
        ContactSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    return submission


@router.patch("/submissions/{submission_id}", response_model=ContactSubmissionResponse)
def update_contact_submission(
    submission_id: str,
    update_data: ContactSubmissionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """
    Update a contact submission status/notes (admin only).
    """
    submission = db.query(ContactSubmission).filter(
        ContactSubmission.id == submission_id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Update fields
    if update_data.status is not None:
        submission.status = update_data.status
    if update_data.assigned_to is not None:
        submission.assigned_to = update_data.assigned_to
    if update_data.notes is not None:
        submission.notes = update_data.notes
    
    db.commit()
    db.refresh(submission)
    
    return submission
