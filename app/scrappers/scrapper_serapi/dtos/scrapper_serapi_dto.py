from pydantic import BaseModel

class GoogleMapsRequestDTO(BaseModel):
    termo: str


class GoogleMapsExcelResponseDTO(BaseModel):
    termo: str
    quantidade: int
    arquivo: str
