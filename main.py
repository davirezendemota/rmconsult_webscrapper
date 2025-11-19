from fastapi import FastAPI
from app.routers import register_routes
from app.core.logger import setup_logging

# Inicializar sistema de logging (envia logs para stdout/stderr para Docker)
setup_logging()

app = FastAPI(
    title="RM CONSULT – Scrappers",
    description="Coleção de scrappers (Google Maps, Google Places, etc) padronizados",
    version="1.0.0",
)

register_routes(app)
