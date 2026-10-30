from typing import Protocol
from uuid import UUID


class AuthError(Exception):
    pass


class InvalidTokenError(AuthError):
    pass


class TokenExpiredError(AuthError):
    pass


class CannotRefreshSession(AuthError):
    pass


class AuthTokenService(Protocol):
    async def create_session(self, *, user_id: UUID) -> tuple[str, str]:
        """Creates a session pair: (access_token_jwt, refresh_token_jwt)"""
        ...

    async def verify_access_token(self, *, token: str) -> UUID:
        """
        Validates an Access JWT & returns a user UUID.

        Raises:
            InvalidTokenError: If signature is bad or payload is invalid.
            TokenExpiredError: If token expiration time (exp) has passed.
        """
        ...

    async def refresh_session(self, *, old_refresh_token: str) -> tuple[str, str]:
        """
        Checks an old token and returns a new pair.

        Raises:
            CannotRefreshSession: If session expired or doesn't exist.
        """
        ...

    async def delete_session(self, *, refresh_token: str) -> None: ...
