from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from hobby_tracker_api.ports.auth import AuthTokenService, CannotRefreshSession
from hobby_tracker_api.schemas import Token

from .router import auth_router


class RefreshForm(BaseModel):
    refresh_token: str


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_user_session(
    form_data: RefreshForm,
    token_service: Annotated[AuthTokenService, Depends()],
) -> Token:
    try:
        new_access_token, new_refresh_token = await token_service.refresh_session(
            old_refresh_token=form_data.refresh_token
        )
    except CannotRefreshSession:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )
