import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")

    @property
    def SERPAPI_KEYS_LIST(self):
        return [k.strip() for k in self.SERPAPI_KEY.split(",")]
    
    class Config:
        env_file = ".env"

env = Env()
