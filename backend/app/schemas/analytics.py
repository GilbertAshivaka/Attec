from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID


# Request schemas
class AnalyticsEventCreate(BaseModel):
    event_type: str = Field(..., min_length=1, max_length=50)
    event_data: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    referrer: Optional[str] = None


# Response schemas
class AnalyticsEventResponse(BaseModel):
    id: UUID
    event_type: str
    event_data: Optional[Dict[str, Any]]
    session_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    referrer: Optional[str]
    timestamp: datetime
    
    model_config = {"from_attributes": True}


class AnalyticsSummary(BaseModel):
    total_events: int
    total_submissions: int
    unique_sessions: int
    date_range: Dict[str, date]
    top_events: list[Dict[str, Any]]
    submissions_by_status: Dict[str, int]
