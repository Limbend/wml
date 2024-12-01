import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str
    echo: bool = True

    @property
    def connection_url(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class S3Config(BaseModel):
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BACKEND__",
    )

    db: DatabaseConfig
    s3: S3Config
    origins: list[str]

    @property
    def logging_config(self):
        log_dir = "./logs"
        os.makedirs(log_dir, exist_ok=True)

        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "standard": {
                    "format": "%(asctime)-23s - %(levelname)-8s - %(name)-24s - %(message)s"
                },
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
                    "filename": f"{log_dir}/wml.info.log",
                    "mode": "a",
                    "maxBytes": 1048576,
                    "backupCount": 3,
                },
            },
            "loggers": {
                "": {  # root logger
                    "level": "INFO",
                    "handlers": ["default", "info_rotating_file_handler"],
                    "propagate": False,
                },
                "repository": {
                    "level": "INFO",
                    "handlers": ["default", "info_rotating_file_handler"],
                    "propagate": False,
                },
                "schemas": {
                    "level": "INFO",
                    "handlers": ["default", "info_rotating_file_handler"],
                    "propagate": False,
                },
                "s3": {
                    "level": "INFO",
                    "handlers": ["default", "info_rotating_file_handler"],
                    "propagate": False,
                },
                "sqlalchemy.engine.Engine": {
                    "level": "INFO",
                    "handlers": ["default", "info_rotating_file_handler"],
                    "propagate": False,
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
