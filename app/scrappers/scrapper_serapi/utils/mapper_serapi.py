from datetime import datetime
from app.scrappers.scrapper_serapi.scrapper_serapi_dto import CompanyInfoDTO


def map_serapi_to_company_info(item: dict) -> CompanyInfoDTO:
    address = item.get("address", "")

    # Dividir endereço (quando possível) — mapeamento inteligente
    neighborhood = None
    city = None
    state = None
    zip_code = None

    if address and "," in address:
        parts = [p.strip() for p in address.split(",")]
        if len(parts) >= 2:
            neighborhood = parts[1]
        if len(parts) >= 3:
            city = parts[2].split("-")[0].strip()
        if len(parts) >= 3 and "-" in parts[2]:
            state = parts[2].split("-")[1].strip()

        if len(parts) >= 4:
            zip_code = parts[3].replace("Brasil", "").strip()

    dto = CompanyInfoDTO(
        # Basic
        name=item.get("title"),
        line_of_business=item.get("type"),
        maps_category=item.get("types", [None])[0],
        description=item.get("user_review"),

        # Location
        address=address,
        neighborhood=neighborhood,
        city=city,
        state=state,
        region=None,
        country="Brasil",
        zip_code=zip_code,

        # Contact
        phone_number=item.get("phone"),
        email=None,
        website=item.get("website"),
        has_website=item.get("website") is not None,

        # Digital presence
        url_google_maps=item.get("place_id_search"),
        place_id=item.get("place_id"),
        review_count=item.get("reviews"),
        rating=item.get("rating"),
        business_hours=item.get("opening_hours"),
        photos_url=[item.get("thumbnail")] if item.get("thumbnail") else [],

        # Comercial
        price_range=item.get("price_level"),

        # Metadata
        data_scraping=datetime.utcnow(),
        last_updated=datetime.utcnow(),
    )

    return dto
