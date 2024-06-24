import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # MySQL settings
    mysql_user: str = os.getenv("MYSQL_USER")
    mysql_password: str = os.getenv("MYSQL_PASSWORD")
    mysql_db: str = os.getenv("MYSQL_DATABASE")
    mysql_host: str = os.getenv("MYSQL_HOST")
    mysql_port: str = os.getenv("MYSQL_PORT")
    db_uri: str = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"

settings = Settings()