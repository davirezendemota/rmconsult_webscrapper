from serpapi import GoogleSearch
from app.core.config import env
from app.core.logger import serpapi_logger


class SerApiScraper:

    @staticmethod
    def buscar_api(termo: str):
        """
        Busca empresas no Google Maps via SerpAPI.
        Registra logs de cada consumo da API.
        """
        params = {
            "engine": "google_maps",
            "q": termo,
            "hl": "pt-br",
            "api_key": env.SERPAPI_KEY,
        }

        # Log: Início da chamada à SerpAPI
        serpapi_logger.info(
            f"SerpAPI: Iniciando busca - termo='{termo}', engine='google_maps'"
        )

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            empresas = results.get("local_results", [])
            meta = results.get("search_metadata", {})

            # Extrair informações relevantes dos metadados
            status = meta.get("status", "unknown")
            total_results = len(empresas)
            search_id = meta.get("id", "N/A")
            created_at = meta.get("created_at", "N/A")

            # Log: Sucesso na chamada
            serpapi_logger.info(
                f"SerpAPI: Busca concluída com sucesso - "
                f"termo='{termo}', "
                f"status='{status}', "
                f"total_resultados={total_results}, "
                f"search_id='{search_id}', "
                f"created_at='{created_at}'"
            )

            return empresas, meta

        except Exception as e:
            # Log: Erro na chamada
            serpapi_logger.error(
                f"SerpAPI: Erro ao buscar - termo='{termo}', "
                f"erro='{str(e)}', tipo='{type(e).__name__}'"
            )
            raise
