from datetime import date
from typing import Annotated, Self

from fastapi import Depends, status
from hobby_tracker.application import QueryBus
from hobby_tracker.application.queries import HobbiesStatsQuery, HobbiesStatsView
from pydantic import BaseModel

from hobby_tracker_api.dependencies.application import get_query_bus

from .router import hobby_router
from .schemas import HobbyStats, Stats


class HobbiesStatsResponse(BaseModel):
    hobbies_stats: list[HobbyStats]
    common_stats: Stats

    @classmethod
    def from_view(cls, view: HobbiesStatsView) -> Self:
        return cls(
            hobbies_stats=[
                HobbyStats.from_applicationDTO(dto) for dto in view.hobbies_stats
            ],
            common_stats=Stats.from_applicationDTO(view.common_stats),
        )


@hobby_router.get("/stats", status_code=status.HTTP_200_OK)
def get_hobbies_stats(
    date_from: date,
    date_to: date,
    query_bus: Annotated[QueryBus, Depends(get_query_bus)],
) -> HobbiesStatsResponse:

    query = HobbiesStatsQuery(date_from=date_from, date_to=date_to)
    view = query_bus(query)

    return HobbiesStatsResponse.from_view(view)
