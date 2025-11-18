from serpapi import GoogleSearch
from app.core.config import env


class SerApiScraper:

    @staticmethod
    def buscar_api(termo: str):
        params = {
            "engine": "google_maps",
            "q": termo,
            "hl": "pt-br",
            "api_key": env.SERPAPI_KEY,
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        empresas = results.get("local_results", [])
        meta = results.get("search_metadata", {})

        return empresas, meta
