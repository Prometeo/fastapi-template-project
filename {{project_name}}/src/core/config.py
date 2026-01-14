from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    APP_NAME: str = "Example Project"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/foobar"
    DATABASE_TEST_URL: str = "postgresql://user:pass@localhost:5433/foobar"
    SECRET_KEY: str = "CHANGE ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    LOG_LEVEL: str = "INFO"
    ENV: str = "dev"

    model_config: SettingsConfigDict = SettingsConfigDict(env_prefix="EXAMPLE_", case_sensitive=True)


config = Config()
