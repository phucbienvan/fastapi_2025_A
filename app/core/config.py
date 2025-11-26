import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")

settings = Settings()
