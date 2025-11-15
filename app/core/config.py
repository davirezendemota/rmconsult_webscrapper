import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")

settings = Settings()
