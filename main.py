from fastapi import FastAPI
from app.routers import register_routes

app = FastAPI(
    title="RM CONSULT – Scrappers",
    description="Coleção de scrappers (Google Maps, Google Places, etc) padronizados",
    version="1.0.0",
)

register_routes(app)
