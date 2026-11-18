from uuid import UUID, uuid7

from hobby_tracker_infrastructure.persistence.sqlalchemy import models
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from hobby_tracker_api.ports import user


class SQLAlchemyUserService:
    def __init__(self, session: Session):
        self._session = session
        self._hasher = PasswordHash.recommended()

    async def register(self, *, username: str, user_id: UUID, password: str) -> None:
        user_id = uuid7()
        try:
            with self._session.begin():
                user_model = models.User(
                    id=user_id,
                    username=username,
                    password_hash=self._hasher.hash(password),
                )
                self._session.add(user_model)
        except IntegrityError:
            raise user.UsernameExists

    async def authorize(self, *, username: str, password: str) -> UUID:
        stmt = select(models.User).where(models.User.username == username)
        user_model = self._session.scalar(stmt)
        if user_model is None:
            raise user.AuthorizeError
        is_valid = self._hasher.verify(password, user_model.password_hash)
        if not is_valid:
            raise user.AuthorizeError

        return user_model.id
