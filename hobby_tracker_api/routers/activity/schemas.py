from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Activity(BaseModel):
    activity_id: UUID
    hobby_id: UUID
    duration_minutes: int
    started_at: datetime
    note: str | None
