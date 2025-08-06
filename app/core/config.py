from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Time-Off Policy App"
