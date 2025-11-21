from fastapi import FastAPI
from app.scrappers.scrapper_serapi.serapi_controller import serapi_router

def register_routes(app: FastAPI):
    app.include_router(serapi_router, prefix="/scraper/serapi")
