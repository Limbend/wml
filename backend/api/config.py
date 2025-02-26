import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


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

    launch_mode: str
    db: DatabaseConfig
    s3: S3Config
    origins: list[str]
    log_cfg: str = "logging_config.json"

    @property
    def logging_config(self):
        log_dir = "./logs"
        os.makedirs(log_dir, exist_ok=True)

        with open(self.log_cfg) as f:
            config = json.load(f)

        return config


settings = Settings()
