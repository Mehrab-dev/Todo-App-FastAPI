from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Setting(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str = "9c1d66dddfc5071c928b0945b2746e6e7bac643e808d63d90748e8b34ffa02cb"


setting = Setting()