from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/app.db"
    JWT_SECRET: str = "change-me"
    JWT_ALGO: str = "HS256"
    JWT_EXPIRES_MIN: int = 480
    ADMIN_EMAIL: str = "admin@khenifra.local"
    ADMIN_PASSWORD: str = "Admin@2026"
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
