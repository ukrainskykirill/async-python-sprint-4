from pydantic import BaseSettings, PostgresDsn
from dotenv import load_dotenv

load_dotenv()


class AppSettings(BaseSettings):
    app_title: str
    database_dsn: PostgresDsn
    host: str
    port: int
    blocked_host: list

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


app_settings = AppSettings()
