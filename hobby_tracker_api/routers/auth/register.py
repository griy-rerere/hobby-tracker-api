from typing import Annotated
from uuid import uuid7

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from hobby_tracker_api.ports.auth import AuthTokenService
from hobby_tracker_api.ports.user import UsernameExists, UserService
from hobby_tracker_api.schemas import Token

from .router import auth_router


class RegistrationForm(BaseModel):
    username: str
    password: str


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    form_data: RegistrationForm,
    user_service: Annotated[UserService, Depends()],
    token_service: Annotated[AuthTokenService, Depends()],
) -> Token:
    user_id = uuid7()
    try:
        await user_service.register(
            username=form_data.username, user_id=user_id, password=form_data.password
        )
    except UsernameExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    access_token, refresh_token = await token_service.create_session(user_id=user_id)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
