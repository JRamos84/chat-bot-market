import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}"
}


def fetch_from_supabase(endpoint: str) -> list:
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise ConnectionError(f"❌ Error {response.status_code}: {response.text}")
    
    return response.json()


def guardar_json(data: list, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Archivo guardado como {path}")


def get_conversations_by_session(session_id: str) -> None:
    data = fetch_from_supabase(f"n8n_chat_histories?session_id=eq.{session_id}&select=*")
    if data:
        guardar_json(data, f"data/conversaciones/conversaciones_session_{session_id}.json")
    else:
        print("⚠️ No se encontraron datos para ese session_id.")


def get_all_usuarios() -> None:
    data = fetch_from_supabase("usuarios?select=*")
    if data:
        guardar_json(data, "data/usuarios/usuarios.json")
    else:
        print("⚠️ No se encontraron usuarios.")
