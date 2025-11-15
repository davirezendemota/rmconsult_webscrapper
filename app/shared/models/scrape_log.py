from app.core.BaseModel import BaseModel

class ScrapeLog(BaseModel):
    termo: str
    quantidade: int
    meta: dict
