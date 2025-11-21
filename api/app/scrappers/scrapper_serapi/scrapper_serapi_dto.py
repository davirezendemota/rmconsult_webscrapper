from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class SerApiBuscarDTO(BaseModel):
    termo: str

class CompanyInfoDTO(BaseModel):
    # Basic identification
    name: Optional[str]
    line_of_business: Optional[str]
    maps_category: Optional[str]
    description: Optional[str]

    # Location
    address: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    state: Optional[str]
    region: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]

    # Contact
    phone_number: Optional[str]
    email: Optional[str]
    website: Optional[str]
    has_website: Optional[bool]

    # Digital presence
    url_google_maps: Optional[str]
    place_id: Optional[str]
    review_count: Optional[int]
    rating: Optional[float]
    business_hours: Optional[Dict[str, Any]]
    photos_url: Optional[List[str]]

    # Comercial info
    price_range: Optional[str]

    # Metadata
    data_scraping: datetime
    source: str = "google_maps"
    last_updated: datetime