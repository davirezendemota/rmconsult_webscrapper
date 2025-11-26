from datetime import datetime
from scrappers.scrapper_serapi.dtos.scrapper_serapi_dto import CompanyInfoDTO


def map_serapi_to_company_info(item: dict) -> CompanyInfoDTO:
    print(item)
    print('')
    address = item.get("address", "")

    if address and "," in address:
        parts = [p.strip() for p in address.split(",")]
        if len(parts) >= 1:
            country = parts[-1]
            
    dto = CompanyInfoDTO(
        # Basic
        name=item.get("title"),
        line_of_business=item.get("type"),
        maps_category=item.get("types", [None])[0],
        description=item.get("user_review"),

        # Location
        address=address,
        neighborhood=None,
        city=None,
        state=None,
        region=None,
        country=country,
        zip_code=None,

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
