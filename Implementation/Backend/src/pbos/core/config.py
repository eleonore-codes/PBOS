from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    app_name: str = "PBOS Core API"
    api_version: str = "0.2.0"
    database_url: str = "sqlite:///./pbos_m2.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()
