from fastapi import FastAPI
from scrappers.scrapper_serapi.controllers.serapi_controller import serapi_router


def register_routes(app: FastAPI):
    app.include_router(serapi_router, prefix="/scraper/serapi")
    
