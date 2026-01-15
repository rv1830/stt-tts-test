import httpx
from app.core.config import settings

class ProKeralaService:
    def __init__(self):
        self.client_id = settings.PROKERALA_CLIENT_ID
        self.client_secret = settings.PROKERALA_CLIENT_SECRET

    async def get_token(self):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.prokerala.com/token", data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            })
            return resp.json().get("access_token")

    async def get_kundli_data(self, params: dict):
        token = await self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            res = await client.get("https://api.prokerala.com/v2/astrology/panchang", 
                                    params=params, headers=headers)
            return res.json()