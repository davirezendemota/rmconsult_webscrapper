from datetime import datetime
from app.scrappers.scrapper_serapi.mapper_serapi import map_serapi_to_company_info
from app.scrappers.scrapper_serapi.utils.credits import update_credit_usage
from app.scrappers.scrapper_serapi.serapi_scraper import SerApiScraper
from app.scrappers.scrapper_serapi.utils.excel_formatter import ExcelFormatter
from app.scrappers.scrapper_serapi.serapi_repository import SerApiRepository


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
        # Busca empresas
        empresas, meta = SerApiScraper.buscar_api(termo)

        # Gera excel
        arquivo = ExcelFormatter.gerar_excel(empresas, termo)

        return {
            "termo": termo,
            "quantidade": len(empresas),
            "arquivo": arquivo,
            "meta": meta,
        }
