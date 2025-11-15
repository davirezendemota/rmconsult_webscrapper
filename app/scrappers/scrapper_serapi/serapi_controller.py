from fastapi import APIRouter, Depends
from app.scrappers.scrapper_serapi import scrapper_serapi_dto
from app.scrappers.scrapper_serapi import serapi_service

serapi_router = APIRouter(tags=["SerAPI Google Maps"])


@serapi_router.post("/buscar")
def buscar(data: scrapper_serapi_dto, service: serapi_service = Depends()):
    return service.buscar(data.termo)


@serapi_router.post("/buscar/excel")
def buscar_excel(data: scrapper_serapi_dto, service: serapi_service = Depends()):
    return service.buscar_excel(data.termo)
