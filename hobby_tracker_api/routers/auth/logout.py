from typing import Annotated

from fastapi import Depends, status
from pydantic import BaseModel

from hobby_tracker_api.ports.auth import AuthTokenService

from .router import auth_router


class LogoutForm(BaseModel):
    refresh_token: str


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    form_data: LogoutForm,
    token_service: Annotated[AuthTokenService, Depends()],
) -> None:
    await token_service.delete_session(refresh_token=form_data.refresh_token)
