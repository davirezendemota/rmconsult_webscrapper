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

        # Atualiza créditos
        # used, limit = update_credit_usage(termo)

        # Salva log
        # self.repo.save_log(
        #     termo_busca=termo,
        #     quantidade=len(empresas),
        #     meta=meta
        # )

        return {
            "termo": termo,
            "quantidade": len(empresas),
            "meta": meta,
            # "credits": {"used": used, "limit": limit},
            "empresas": empresas
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
