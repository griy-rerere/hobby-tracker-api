from typing import Protocol
from uuid import UUID


class UserServiceException(Exception):
    pass


class UsernameExists(UserServiceException):
    pass


class AuthorizeError(UserServiceException):
    pass


class UserService(Protocol):
    async def register(
        self, *, username: str, user_id: UUID, password: str
    ) -> None: ...

    async def authorize(self, *, username: str, password: str) -> UUID: ...
