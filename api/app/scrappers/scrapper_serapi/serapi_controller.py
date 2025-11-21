from fastapi import APIRouter, Depends
from typing import Dict, Any
from fastapi.responses import FileResponse
from app.scrappers.scrapper_serapi.scrapper_serapi_dto import SerApiBuscarDTO
from app.scrappers.scrapper_serapi.serapi_service import SerApiService

serapi_router = APIRouter(tags=["SerAPI Google Maps"])

@serapi_router.post("/buscar")
def buscar(data: SerApiBuscarDTO, service: SerApiService = Depends()) -> Dict[str, Any]:
    """
    Busca empresas no Google Maps via SerpAPI.
    Retorna dados padronizados no formato do modelo `company_info`.
    """
    return service.buscar(data.termo)


@serapi_router.post("/buscar/excel")
def buscar_excel(data: SerApiBuscarDTO, service: SerApiService = Depends()):
    return service.buscar_excel(data.termo)
