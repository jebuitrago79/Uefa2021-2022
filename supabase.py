import httpx
import asyncio

SUPABASE_URL = "https://vjcbkkaimpzzyhuczoej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZqY2Jra2FpbXB6enlodWN6b2VqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkwMDMyMjMsImV4cCI6MjA2NDU3OTIyM30.ByyZph5pFmCO9LGOfhrcgyeuU8JqtE3-lkhbNAYQ45c"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}
async def test_supabase_connection():
    async with httpx.AsyncClient() as client:
        url = f"{SUPABASE_URL}/rest/v1/player_images?sofifa_id=eq.2147&select=*"
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 200:
            print("✅ Conexión exitosa con Supabase")
            print("🔍 Resultado:", response.json())
        else:
            print(f"❌ Error al conectar. Código: {response.status_code}")
            print("Respuesta:", response.text)

async def get_player_images(sofifa_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        url = f"{SUPABASE_URL}/rest/v1/player_images?sofifa_id=eq.{sofifa_id}&select=*"
        response = await client.get(url, headers=HEADERS)
        if response.status_code == 200 and response.json():
            return response.json()[0]
        return {}



if __name__ == "__main__":
    asyncio.run(test_supabase_connection())
