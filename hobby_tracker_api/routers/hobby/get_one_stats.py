from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from hobby_tracker.application import QueryBus
from hobby_tracker.application.queries import HobbyStatsQuery
from hobby_tracker.domain.exceptions import HobbyNotFound

from hobby_tracker_api.dependencies.application import get_query_bus

from .router import hobby_router
from .schemas import HobbyStats


@hobby_router.get("/{hobby_id}/stats", status_code=status.HTTP_200_OK)
def get_hobby_stats(
    hobby_id: UUID,
    date_from: date,
    date_to: date,
    query_bus: Annotated[QueryBus, Depends(get_query_bus)],
) -> HobbyStats:
    try:
        query = HobbyStatsQuery(hobby_id=hobby_id, date_from=date_from, date_to=date_to)
        view = query_bus(query)
    except HobbyNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return HobbyStats.from_applicationDTO(view.stats)
