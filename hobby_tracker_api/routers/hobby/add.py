from typing import Annotated
from uuid import UUID, uuid7

from fastapi import Depends, HTTPException, Response, status
from hobby_tracker.application import CommandBus
from hobby_tracker.application.commands import AddHobbyCommand
from hobby_tracker.domain.exceptions import HobbyAttributeDuplicate
from hobby_tracker_api.dependencies.application import get_command_bus
from pydantic import BaseModel

from .router import hobby_router


class AddHobbyRequest(BaseModel):
    name: str


class AddHobbyResponse(BaseModel):
    name: str
    id: UUID


@hobby_router.post("", status_code=status.HTTP_201_CREATED)
def add_hobby(
    request: AddHobbyRequest,
    command_bus: Annotated[CommandBus, Depends(get_command_bus)],
    response: Response,
) -> AddHobbyResponse:
    try:
        new_id = uuid7()
        command = AddHobbyCommand(id=new_id, name=request.name)
        command_bus(command)
    except HobbyAttributeDuplicate as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    response.headers["Location"] = f"{hobby_router.prefix}/{new_id}"
    return AddHobbyResponse(name=request.name, id=new_id)
