from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Em Docker, o docker-compose injeta DATABASE_URL apontando para o Postgres.
    # Fora do Docker, cai num SQLite local (sem credenciais) para desenvolvimento.
    database_url: str = "sqlite:///./pokemon.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
