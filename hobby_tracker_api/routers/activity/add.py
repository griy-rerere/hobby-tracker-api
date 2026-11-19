from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid7

from fastapi import Depends, HTTPException, Response, status
from hobby_tracker.application import CommandBus
from hobby_tracker.application.commands import AddActivityCommand
from hobby_tracker.domain.exceptions import ActivityAttributeDuplicate, HobbyNotFound
from pydantic import BaseModel

from hobby_tracker_api.dependencies.application import get_command_bus

from .router import activity_router
from .schemas import Activity


class AddActivityRequest(BaseModel):
    hobby_id: UUID
    duration_minutes: int
    started_at: datetime
    note: str | None


@activity_router.post("", status_code=status.HTTP_201_CREATED)
def add_activity(
    request: AddActivityRequest,
    command_bus: Annotated[CommandBus, Depends(get_command_bus)],
    response: Response,
) -> Activity:
    try:
        new_id = uuid7()
        command = AddActivityCommand(
            activity_id=new_id,
            hobby_id=request.hobby_id,
            started_at=request.started_at,
            duration_minutes=request.duration_minutes,
            note=request.note,
        )
        command_bus(command)
    except HobbyNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ActivityAttributeDuplicate as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    response.headers["Location"] = f"{activity_router.prefix}/{new_id}"
    return Activity(
        activity_id=new_id,
        hobby_id=request.hobby_id,
        started_at=request.started_at,
        duration_minutes=request.duration_minutes,
        note=request.note,
    )
