import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")

env = Env()
