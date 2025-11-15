import os
import sys
import json
from datetime import datetime

# Caminho da pasta onde o .py ou .exe está rodando
BASE_DIR = os.path.dirname(sys.argv[0])
CREDITS_FILE = os.path.join(BASE_DIR, "credits.json")

# Dados padrão
DEFAULT_DATA = {
    "credits_used": 2,
    "credits_limit": 250,
    "last_query": "barbearia recife",
    "last_reset": datetime.now().strftime("%Y-%m")  # ano-mes
}

def save_credits(data):
    with open(CREDITS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_credits():
    """Carrega o JSON e aplica reset mensal automaticamente."""
    # Se não existe, cria agora
    if not os.path.exists(CREDITS_FILE):
        save_credits(DEFAULT_DATA)
        return DEFAULT_DATA

    try:
        with open(CREDITS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        # Arquivo corrompido
        save_credits(DEFAULT_DATA)
        return DEFAULT_DATA

    # ----- RESET AUTOMÁTICO MENSAL -----
    mes_atual = datetime.now().strftime("%Y-%m")
    mes_salvo = data.get("last_reset", mes_atual)

    if mes_atual != mes_salvo:
        # Reset
        data["credits_used"] = 0
        data["last_reset"] = mes_atual
        save_credits(data)

    return data


def update_credit_usage(query):
    data = load_credits()

    # só conta se a consulta for diferente
    if query != data.get("last_query"):
        data["credits_used"] += 1

    data["last_query"] = query
    save_credits(data)

    return data["credits_used"], data["credits_limit"]
