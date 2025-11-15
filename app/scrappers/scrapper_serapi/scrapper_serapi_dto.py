from pydantic import BaseModel

class SerApiBuscarDTO(BaseModel):
    termo: str


class GoogleMapsExcelResponseDTO(BaseModel):
    termo: str
    quantidade: int
    arquivo: str
