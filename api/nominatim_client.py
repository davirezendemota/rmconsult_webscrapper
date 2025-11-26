import httpx
import time

class NominatimClient:
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    @staticmethod
    def geocode(address: str) -> dict | None:
        params = {
            "q": address,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }

        headers = {
            "User-Agent": "rmconsult-scrappers/1.0 (contato@seudominio.com)"
        }

        time.sleep(1)  # obrigatório para não violar rate limit

        try:
            resp = httpx.get(NominatimClient.BASE_URL, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            print(data)
            print('')
            return data[0] if data else None
        except Exception:
            return None