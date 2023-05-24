from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None
    MONGO_INITDB_DATABASE: str | None

    JWT_REFRESH_SECRET_KEY: str | None
    JWT_SECRET_KEY: str | None
    REFRESH_TOKEN_EXPIRES_IN: int | None
    ACCESS_TOKEN_EXPIRES_IN: int | None
    JWT_ALGORITHM: str | None

    CLIENT_ORIGIN: str | None

    class Config:
        env_file = '../.env'


settings = Settings()
