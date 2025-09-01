from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "mysql+aiomysql://root:root@localhost:3306/wallet"

    class Config:
        env_file = ".env"

settings = Settings()