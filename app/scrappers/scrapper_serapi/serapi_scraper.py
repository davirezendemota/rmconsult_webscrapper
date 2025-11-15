from serpapi import GoogleSearch
from app.core.config import settings


class SerApiScraper:

    @staticmethod
    def buscar(termo: str):
        params = {
            "engine": "google_maps",
            "q": termo,
            "hl": "pt-br",
            "api_key": settings.SERPAPI_KEY,
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        local_results = results.get("local_results", [])
        meta = results.get("search_metadata", {})

        return local_results, meta
