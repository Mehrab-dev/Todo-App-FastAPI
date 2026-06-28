from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Setting(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = ""
    JWT_SECRET_KEY: str = "60237ee0bd6949a5b8eaf48c457f31fd30e6afa36bf77393dcb2d84efc99f8df"


setting = Setting()