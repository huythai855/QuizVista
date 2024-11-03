import os
from typing import Callable
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        self.BACKEND_PORT = int(os.getenv("BACKEND_PORT"))
        self.SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
        self.SERV_API_KEY = os.getenv("SERV_API_KEY")

def _configure_initial_settings() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()
    def fn() -> Settings:
        return settings
    return fn

get_settings = _configure_initial_settings()