from fastapi import FastAPI
from app.routers import register_routes

app = FastAPI(title="Scraper Hub API")

register_routes(app)
