import httpx
import pytest

SUPABASE_URL = "https://vjcbkkaimpzzyhuczoej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZqY2Jra2FpbXB6enlodWN6b2VqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkwMDMyMjMsImV4cCI6MjA2NDU3OTIyM30.ByyZph5pFmCO9LGOfhrcgyeuU8JqtE3-lkhbNAYQ45c"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}


@pytest.mark.asyncio
async def test_supabase_connection():
    url = f"{SUPABASE_URL}/rest/v1/player_images?sofifa_id=eq.2147&select=*"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=HEADERS)
        assert response.status_code == 200, f"❌ Código de estado inesperado: {response.status_code}"
        print("✅ Conexión exitosa con Supabase")
        print("🔍 Resultado:", response.json())


async def insertar_imagen_supabase(sofifa_id: int, photo_url: str, club_logo_url: str, nationality_flag_url: str):
    url = f"{SUPABASE_URL}/rest/v1/player_images"
    payload = {
        "sofifa_id": sofifa_id,
        "player_face_url": photo_url,
        "club_logo_url": club_logo_url,
        "nation_flag_url": nationality_flag_url
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=payload, headers=HEADERS)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"❌ Error HTTP al insertar en Supabase: {e.response.status_code}")
            print("Contenido de la respuesta:", e.response.text)
            return None

        try:
            return response.json()
        except Exception:
            print("⚠️ La respuesta no contenía JSON.")
            print("Contenido:", response.text)
            return None


async def actualizar_imagen_supabase(sofifa_id: int, bandera_url: str, escudo_url: str):
    url = f"{SUPABASE_URL}/rest/v1/player_images?sofifa_id=eq.{sofifa_id}"
    payload = {
        "nation_flag_url": bandera_url,
        "club_logo_url": escudo_url
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.patch(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()


async def get_player_images(sofifa_id: int) -> dict:
    url = f"{SUPABASE_URL}/rest/v1/player_images?sofifa_id=eq.{sofifa_id}&select=*"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            return data[0] if data else {}
    except httpx.RequestError as e:
        print(f"⚠️ Error de red: {e}")
    except httpx.HTTPStatusError as e:
        print(f"⚠️ Error HTTP: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"⚠️ Otro error: {e}")
    return {}
