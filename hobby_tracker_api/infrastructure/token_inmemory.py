import secrets
from asyncio import Lock
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from uuid import UUID

import jwt

from hobby_tracker_api.ports import auth
from hobby_tracker_api.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    AUTH_ALGORITHM,
    AUTH_SECRET_KEY,
    REFRESH_TOKEN_BYTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


@dataclass(frozen=True, slots=True)
class RefreshSession:
    user_id: UUID
    expires_at: datetime


class InMemoryTokenService:
    def __init__(self) -> None:
        self._refresh_tokens: dict[str, RefreshSession] = {}
        self._lock = Lock()

    @staticmethod
    def _hash_token(token: str) -> str:
        return sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def _create_access_token(*, user_id: UUID) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        return jwt.encode(
            payload,
            AUTH_SECRET_KEY,
            algorithm=AUTH_ALGORITHM,
        )

    @staticmethod
    def _create_refresh_token() -> str:
        return secrets.token_urlsafe(REFRESH_TOKEN_BYTES)

    def _cleanup_expired_sessions(self) -> None:
        now = datetime.now(timezone.utc)

        expired_tokens = [
            token_hash
            for token_hash, session in self._refresh_tokens.items()
            if session.expires_at <= now
        ]

        for token_hash in expired_tokens:
            del self._refresh_tokens[token_hash]

    async def create_session(
        self,
        *,
        user_id: UUID,
    ) -> tuple[str, str]:
        """Creates a session pair: (access_token, refresh_token)."""

        now = datetime.now(timezone.utc)

        access_token = self._create_access_token(user_id=user_id)
        refresh_token = self._create_refresh_token()

        token_hash = self._hash_token(refresh_token)

        async with self._lock:
            self._cleanup_expired_sessions()

            self._refresh_tokens[token_hash] = RefreshSession(
                user_id=user_id,
                expires_at=now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            )

        return access_token, refresh_token

    async def verify_access_token(
        self,
        *,
        token: str,
    ) -> UUID:
        """
        Validates an access JWT and returns its user UUID.

        Raises:
            auth.InvalidTokenError: Invalid token or payload.
            auth.TokenExpiredError: Token has expired.
        """

        try:
            payload = jwt.decode(
                token,
                AUTH_SECRET_KEY,
                algorithms=[AUTH_ALGORITHM],
                options={
                    "require": ["sub", "iat", "exp"],
                },
            )

            user_id = UUID(payload["sub"])

        except jwt.ExpiredSignatureError as exc:
            raise auth.TokenExpiredError from exc

        except (
            jwt.InvalidTokenError,
            ValueError,
            TypeError,
            KeyError,
        ) as exc:
            raise auth.InvalidTokenError from exc

        return user_id

    async def refresh_session(
        self,
        *,
        old_refresh_token: str,
    ) -> tuple[str, str]:
        """
        Validates an old refresh token and rotates the session.

        Raises:
            auth.CannotRefreshSession: Session does not exist
                or has expired.
        """

        old_hash = self._hash_token(old_refresh_token)

        async with self._lock:
            now = datetime.now(timezone.utc)

            session = self._refresh_tokens.pop(old_hash, None)

            if session is None:
                raise auth.CannotRefreshSession

            if session.expires_at <= now:
                raise auth.CannotRefreshSession

            user_id = session.user_id

            access_token = self._create_access_token(user_id=user_id)

            new_refresh_token = self._create_refresh_token()
            new_hash = self._hash_token(new_refresh_token)

            self._refresh_tokens[new_hash] = RefreshSession(
                user_id=user_id,
                expires_at=now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            )

            return access_token, new_refresh_token

    async def delete_session(
        self,
        *,
        refresh_token: str,
    ) -> None:
        """Revokes a session using its refresh token."""

        token_hash = self._hash_token(refresh_token)

        async with self._lock:
            self._refresh_tokens.pop(token_hash, None)
