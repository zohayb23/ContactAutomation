from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "ContactAutomationCloud"
    environment: str = "dev"
    api_token: str = Field(default="change-me", description="Bearer token for protected API routes")

    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/contact_automation"
    redis_url: str = "redis://redis:6379/0"

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_sender_email: str = ""
    smtp_use_tls: bool = True

    dedupe_window_days: int = 14
    default_max_send_per_run: int = 50
    max_requests_per_minute: int = 20


settings = Settings()
