from datetime import datetime

from fastapi.responses import StreamingResponse
from scrappers.scrapper_serapi.utils.mapper_serapi import map_serapi_to_company_info
from scrappers.scrapper_serapi.serapi_scraper import SerApiScraper
from scrappers.scrapper_serapi.utils.excel_formatter import ExcelFormatter
from scrappers.scrapper_serapi.repositories.serapi_repository import SerApiRepository


class SerApiService:

    def __init__(self):
        self.repo = SerApiRepository()

    def buscar(self, termo: str):
        # Executa o scraper
        empresas, meta = SerApiScraper.buscar_api(termo)

        empresas_mapeadas = [map_serapi_to_company_info(e).model_dump() for e in empresas]

        return {
            "status": "ok",
            "termo_busca": termo,
            "quantidade": len(empresas_mapeadas),
            "meta": meta,
            "empresas": empresas_mapeadas,
        }

    def buscar_excel(self, termo: str):
        empresas, meta = SerApiScraper.buscar_api(termo)

        excel_stream = ExcelFormatter.gerar_excel_memoria(empresas, termo)

        nome_limpo = termo.replace(" ", "_").lower()
        filename = f"{nome_limpo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return StreamingResponse(
            excel_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
