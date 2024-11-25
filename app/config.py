from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # AD Configuration
    AD_SERVER: str
    AD_DOMAIN: str
    AD_SUFFIX: str

    class Config:
        env_file = ".env"


settings = Settings()
