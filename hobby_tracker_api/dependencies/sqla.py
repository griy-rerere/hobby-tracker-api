from typing import Annotated, Generator

from fastapi import Depends
from hobby_tracker_infrastructure.persistence.sqlalchemy.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from hobby_tracker_api.settings import DATABASE_URL, MANUAL_MIGRATION

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if not MANUAL_MIGRATION:
    Base.metadata.create_all(bind=engine)


def get_sqla_session() -> Generator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SQLASession = Annotated[Session, Depends(get_sqla_session)]
