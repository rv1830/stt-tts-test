import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROKERALA_CLIENT_ID = os.getenv("PROKERALA_CLIENT_ID")
    PROKERALA_CLIENT_SECRET = os.getenv("PROKERALA_CLIENT_SECRET")
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()