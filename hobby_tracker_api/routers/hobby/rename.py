from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Response, status
from hobby_tracker.application import CommandBus
from hobby_tracker.application.commands import RenameHobbyCommand
from hobby_tracker.domain.exceptions import HobbyNotFound
from pydantic import BaseModel

from hobby_tracker_api.dependencies.application import get_command_bus

from .router import hobby_router
from .schemas import Hobby


class RenameHobbyRequest(BaseModel):
    name: str


@hobby_router.patch("/{hobby_id}/name", status_code=status.HTTP_200_OK)
def rename_hobby(
    hobby_id: UUID,
    request: RenameHobbyRequest,
    command_bus: Annotated[CommandBus, Depends(get_command_bus)],
    response: Response,
) -> Hobby:
    try:
        command = RenameHobbyCommand(hobby_id=hobby_id, new_name=request.name)
        command_bus(command)
    except HobbyNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    response.headers["Location"] = f"{hobby_router.prefix}/{hobby_id}"
    return Hobby(name=request.name, hobby_id=hobby_id)
