from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from hobby_tracker.application import CommandBus
from hobby_tracker.application.commands import DeleteHobbyCommand
from hobby_tracker.domain.exceptions import HobbyNotFound

from hobby_tracker_api.dependencies.application import get_command_bus

from .router import hobby_router


@hobby_router.delete("/{hobby_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hobby(
    hobby_id: UUID,
    command_bus: Annotated[CommandBus, Depends(get_command_bus)],
) -> None:
    try:
        command = DeleteHobbyCommand(hobby_id=hobby_id)
        command_bus(command)
    except HobbyNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
