from typing import Self
from uuid import UUID

from hobby_tracker.application.common import (
    HobbyStats as CoreHobbyStats,
)
from hobby_tracker.application.common import (
    Stats as CoreStats,
)
from pydantic import BaseModel


class Hobby(BaseModel):
    hobby_id: UUID
    name: str


class HobbyStats(BaseModel):
    hobby_id: UUID
    hobby_name: str
    stats: Stats

    @classmethod
    def from_applicationDTO(cls, dto: CoreHobbyStats) -> Self:
        return cls(
            hobby_id=dto.hobby_id,
            hobby_name=dto.hobby_name,
            stats=Stats.from_applicationDTO(dto.stats),
        )


class Stats(BaseModel):
    total_hours: float
    activities: int
    hours_per_day: float

    @classmethod
    def from_applicationDTO(cls, dto: CoreStats) -> Self:
        return cls(
            total_hours=dto.total_hours,
            activities=dto.activities,
            hours_per_day=dto.hours_per_day,
        )
