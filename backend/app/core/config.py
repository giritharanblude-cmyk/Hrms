from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # App
    app_name: str = "SANGAD"
    app_domain: str = "localhost"
    cors_origins: str = "http://localhost:5173"

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "sangad"
    postgres_user: str = "sangad_app"
    postgres_password: SecretStr = SecretStr("")
    postgres_audit_user: str = "sangad_audit"
    postgres_audit_password: SecretStr = SecretStr("")

    @property
    def database_url(self) -> str:
        pw = self.postgres_password.get_secret_value()
        return f"postgresql+asyncpg://{self.postgres_user}:{pw}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def database_url_sync(self) -> str:
        pw = self.postgres_password.get_secret_value()
        return f"postgresql://{self.postgres_user}:{pw}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # Session
    session_secret_key: SecretStr = SecretStr("")
    session_idle_timeout_minutes: int = 30
    session_cookie_name: str = "sangad_sid"

    # Auth
    auth_password_min_length: int = 8
    auth_otp_length: int = 6
    auth_otp_expiry_minutes: int = 5
    auth_otp_max_attempts: int = 5
    auth_otp_resend_cooldown_seconds: int = 60
    auth_login_lockout_attempts: int = 5
    auth_login_lockout_minutes: int = 15

    # SMTP
    smtp_host: str = "smtp.hostinger.com"
    smtp_port: int = 587
    smtp_user: SecretStr = SecretStr("")
    smtp_password: SecretStr = SecretStr("")
    smtp_from_name: str = "SANGAD Admin"
    smtp_from_email: str = "noreply@sangad.in"
    smtp_throttle_per_hour: int = 30

    # S3
    s3_endpoint: str = ""
    s3_region: str = "ap-south-1"
    s3_bucket: str = "sangad-files"
    s3_access_key_id: SecretStr = SecretStr("")
    s3_secret_access_key: SecretStr = SecretStr("")
    s3_disable_ssl: bool = False
    file_storage_backend: str = "s3"

    # Encryption
    field_encryption_key: SecretStr = SecretStr("")

    # Payslip
    payslip_batch_max: int = 50
    voucher_threshold: int = 2000

    # Extraction
    extraction_backend: str = "llm"
    llm_provider: str = "openai"
    llm_api_key: SecretStr = SecretStr("")
    llm_model: str = "gpt-4o"
    local_ocr_lang: str = "eng+hin"

    # WhatsApp / OpenWA
    openwa_base_url: str = "http://openwa:3000"
    openwa_api_key: SecretStr = SecretStr("")
    openwa_webhook_secret: SecretStr = SecretStr("")
    openwa_session_name: str = "sangad-gateway"
    openwa_reply_timeout_seconds: int = 15
    whatsapp_allowed_numbers: str = ""

    # Queue
    rq_queue_name: str = "sangad-jobs"
    rq_job_timeout: int = 600
    rq_result_ttl: int = 3600

    # Observability
    log_level: str = "INFO"
    log_format: str = "json"
    sentry_dsn: SecretStr = SecretStr("")

    # Master user
    master_username: str = "admin"
    master_password: SecretStr = SecretStr("")
    master_email: str = "admin@sangad.in"


settings = Settings()