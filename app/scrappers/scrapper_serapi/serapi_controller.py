from fastapi import APIRouter, Depends
from app.scrappers.scrapper_serapi.scrapper_serapi_dto import SerApiBuscarDTO
from app.scrappers.scrapper_serapi.serapi_service import SerApiService

serapi_router = APIRouter(prefix="/serapi", tags=["SerAPI Google Maps"])


@serapi_router.post("/buscar")
def buscar(data: SerApiBuscarDTO, service: SerApiService = Depends()):
    return service.buscar(data.termo)


@serapi_router.post("/buscar/excel")
def buscar_excel(data: SerApiBuscarDTO, service: SerApiService = Depends()):
    return service.buscar_excel(data.termo)
