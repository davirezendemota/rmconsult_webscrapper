from serpapi import GoogleSearch
from app.core.config import env
from app.core.logger import serpapi_logger


class SerApiScraper:

    @staticmethod
    def buscar_api(termo: str):
        """
        Executa busca usando um pool de chaves:
        - Tenta cada chave em ordem
        - Se der erro (403, limite, invalid key etc), tenta a próxima
        - Se todas falharem, lança exceção
        """

        keys = env.SERPAPI_KEYS_LIST

        if not keys:
            raise RuntimeError("Nenhuma chave configurada em SERPAPI_KEYS")

        last_error = None

        for index, key in enumerate(keys):
            serpapi_logger.info(
                f"Tentando SerpAPI Key {index+1}/{len(keys)}…"
            )

            params = {
                "engine": "google_maps",
                "q": termo,
                "hl": "pt-br",
                "api_key": key,
            }

            try:
                search = GoogleSearch(params)
                results = search.get_dict()

                # Verifica erros típicos da SerpAPI
                if "error" in results:
                    raise Exception(results["error"])

                empresas = results.get("local_results", [])
                meta = results.get("search_metadata", {})

                serpapi_logger.info(
                    f"SerpAPI: sucesso com a key {index+1} | resultados={len(empresas)}"
                )

                return empresas, meta

            except Exception as e:
                serpapi_logger.error(
                    f"SerpAPI Key {index+1} falhou: {str(e)}"
                )
                last_error = e
                continue  # tenta próxima key

        # Se chegou aqui, todas as keys falharam
        raise RuntimeError(
            f"Todas as chaves SerpAPI falharam ao buscar '{termo}'. "
            f"Último erro: {str(last_error)}"
        )
