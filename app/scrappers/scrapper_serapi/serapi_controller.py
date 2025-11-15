from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.scrappers.scrapper_serapi.scrapper_serapi_dto import SerApiBuscarDTO
from app.scrappers.scrapper_serapi.serapi_service import SerApiService
from app.scrappers.scrapper_serapi.utils.paths import RESULTADOS_DIR

serapi_router = APIRouter(tags=["SerAPI Google Maps"])

@serapi_router.post("/buscar")
def buscar(data: SerApiBuscarDTO, service: SerApiService = Depends()):
    return service.buscar(data.termo)


@serapi_router.post("/buscar/excel")
def buscar_excel(data: SerApiBuscarDTO, service: SerApiService = Depends()):
    return service.buscar_excel(data.termo)


# @serapi_router.get("/download/{filename}")
# def download_excel(filename: str):
#     filepath = RESULTADOS_DIR / filename
#     return FileResponse(filepath, media_type="application/vnd.openxmlformats", filename=filename)