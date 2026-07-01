from fastapi import FastAPI

from pbos.api.v1.router import api_v1_router
from pbos.core.config import get_settings
from pbos.infrastructure.database.base import Base
from pbos.infrastructure.database.session import engine


def create_app(*, create_database: bool = False) -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.api_version)

    if create_database:
        Base.metadata.create_all(bind=engine)

    @app.get("/health", tags=["system"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(api_v1_router, prefix="/api/v1")
    return app


app = create_app()
