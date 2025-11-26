import re
from datetime import datetime
from scrappers.scrapper_serapi.dtos.scrapper_serapi_dto import CompanyInfoDTO


def parse_number_block(block: str):
    """
    Extrai número, complementos e bairro de um bloco como:
    400 - Loja 01 - Galeria Ponto 400 - Espinheiro
    """
    # 1) quebra por " - "
    parts = [p.strip() for p in block.split(" - ")]

    if not parts:
        return None, None, None

    # 2) o primeiro item é sempre o número
    number = parts[0]

    # 3) o último item é sempre o bairro
    neighborhood = parts[-1]

    # 4) tudo entre eles são complementos
    complements = parts[1:-1]

    complement = ", ".join(complements) if complements else None

    return number, complement, neighborhood


def parse_address(address: str):
    """
    Parser completo para endereços no formato Google Maps (Brasil)
    """
    if not address or "," not in address:
        return None, None, None, None, None, None, None, None

    parts = [p.strip() for p in address.split(",")]

    # Itens fixos (direita → esquerda)
    country = parts[-1]
    zip_code = parts[-2]
    city_state = parts[-3]

    # Cidade + Estado
    city, state = [x.strip() for x in city_state.split("-")]

    # Resto é street + número/complemento
    resto = parts[:-3]

    # detectar onde começa o número
    number_index = None
    for i, chunk in enumerate(resto):
        if re.match(r"^\d+", chunk):  # começa com número
            number_index = i
            break

    if number_index is None:
        # caso raro: endereço sem número
        street = ", ".join(resto)
        return street, None, None, None, city, state, zip_code, country

    # Rua pode ser um ou vários pedaços antes do número
    street = ", ".join(resto[:number_index]).strip()

    # Bloco com número + complementos + bairro
    num_block = resto[number_index]

    number, complement, neighborhood = parse_number_block(num_block)

    # Pode haver complementos adicionais após o bloco
    if number_index + 1 < len(resto):
        extra_complements = [p.strip() for p in resto[number_index + 1:]]
        if complement:
            complement = complement + ", " + ", ".join(extra_complements)
        else:
            complement = ", ".join(extra_complements)

    return street, number, complement, neighborhood, city, state, zip_code, country


def map_serapi_to_company_info(item: dict) -> CompanyInfoDTO:
    address = item.get("address", "")

    street, number, complement, neighborhood, city, state, zip_code, country = parse_address(address)

    dto = CompanyInfoDTO(
        name=item.get("title"),
        line_of_business=item.get("type"),
        maps_category=item.get("types", [None])[0],
        description=item.get("user_review"),

        address=address,
        neighborhood=neighborhood,
        city=city,
        state=state,
        region=None,
        country=country,
        zip_code=zip_code,

        phone_number=item.get("phone"),
        email=None,
        website=item.get("website"),
        has_website=item.get("website") is not None,

        url_google_maps=item.get("place_id_search"),
        place_id=item.get("place_id"),
        review_count=item.get("reviews"),
        rating=item.get("rating"),
        business_hours=item.get("opening_hours"),
        photos_url=[item.get("thumbnail")] if item.get("thumbnail") else [],

        price_range=item.get("price_level"),

        data_scraping=datetime.utcnow(),
        last_updated=datetime.utcnow(),
    )

    return dto
