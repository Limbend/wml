import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BACKEND_DB_HOST: str
    BACKEND_DB_PORT: int
    BACKEND_DB_NAME: str
    BACKEND_DB_USER: str
    BACKEND_DB_PASS: str

    BACKEND_ORIGINS: list[str]

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.BACKEND_DB_USER}:{self.BACKEND_DB_PASS}@{self.BACKEND_DB_HOST}:{self.BACKEND_DB_PORT}/{self.BACKEND_DB_NAME}"

    @property
    def CORS_ORIGINS(self):
        return self.BACKEND_ORIGINS

    @property
    def LOGGING_CONFIG(self):
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "standard": {"format": "%(asctime)-23s - %(levelname)-8s - %(name)-24s - %(message)s"},
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",  # Default is stderr
                },
                "info_rotating_file_handler": {
                    "level": "INFO",
                    "formatter": "standard",
                    "class": "logging.handlers.RotatingFileHandler",
                    'filename': './logs/wml.info.log',
                    'mode': 'a',
                    'maxBytes': 1048576,
                    'backupCount': 3
                }
            },
            "loggers": {
                "": {  # root logger
                    "level":  "INFO",
                    "handlers": ["default", "info_rotating_file_handler"],
                    "propagate": False,
                },
                "sqlalchemy.engine.Engine": {
                    "level": "INFO",
                    "handlers": ["default", "info_rotating_file_handler"],
                },
                "uvicorn.error": {
                    "level": "DEBUG",
                    "handlers": ["default", "info_rotating_file_handler"],
                },
                "uvicorn.access": {
                    "level": "DEBUG",
                    "handlers": ["default", "info_rotating_file_handler"],
                },
            },
        }


settings = Settings()
