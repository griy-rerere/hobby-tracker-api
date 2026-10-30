from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from hobby_tracker_api.ports.auth import AuthTokenService
from hobby_tracker_api.ports.user import AuthorizeError, UserService
from hobby_tracker_api.schemas import Token

from .router import auth_router


class LoginForm(BaseModel):
    username: str
    password: str


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login_user(
    form_data: LoginForm,
    user_service: Annotated[UserService, Depends()],
    token_service: Annotated[AuthTokenService, Depends()],
) -> Token:
    try:
        user_id = await user_service.authorize(
            username=form_data.username, password=form_data.password
        )
    except AuthorizeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = await token_service.create_session(user_id=user_id)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )
