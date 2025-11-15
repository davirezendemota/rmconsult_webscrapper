class SerApiRepository:
    def save_log(self, termo: str, count: int, meta: dict):
        return {
            "termo": termo,
            "quantidade": count,
            "meta": meta
        }
