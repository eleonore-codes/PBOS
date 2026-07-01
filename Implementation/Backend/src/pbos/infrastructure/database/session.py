from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from pbos.core.config import get_settings


engine = create_engine(get_settings().database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
