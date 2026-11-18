from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from hobby_tracker_api.infrastructure import InMemoryTokenService, SQLAlchemyUserService
from hobby_tracker_api.ports.auth import (
    AuthTokenService,
    InvalidTokenError,
    TokenExpiredError,
)
from hobby_tracker_api.ports.user import UserService

from .sqla import SQLASession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

token_service = InMemoryTokenService()


def get_token_service() -> AuthTokenService:
    return token_service


def get_user_service(session: SQLASession) -> UserService:
    return SQLAlchemyUserService(session=session)


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[AuthTokenService, Depends(get_token_service)],
) -> UUID:
    try:
        user_id = await token_service.verify_access_token(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Access token has expired"
        )
    return user_id


CurrentUserID = Annotated[UUID, Depends(get_current_user_id)]
