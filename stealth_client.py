import asyncio
import random
from curl_cffi.requests import AsyncSession

class StealthClient:
    def __init__(self, impersonate: str = "chrome120"):
        self.impersonate = impersonate
        self.session = AsyncSession(impersonate=self.impersonate)

    def _get_default_headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }

    async def get(self, url: str, retries: int = 3, **kwargs):
        headers = self._get_default_headers()
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        for attempt in range(1, retries + 1):
            try:
                response = await self.session.get(url, headers=headers, **kwargs)
                if response.status_code in [429, 503] and attempt < retries:
                    backoff = (2 ** attempt) + random.uniform(0.5, 1.5)
                    await asyncio.sleep(backoff)
                    continue
                return response
            except Exception as e:
                if attempt == retries:
                    raise e
                await asyncio.sleep(1.0)

    async def post(self, url: str, data=None, json=None, retries: int = 3, **kwargs):
        headers = self._get_default_headers()
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        for attempt in range(1, retries + 1):
            try:
                response = await self.session.post(url, data=data, json=json, headers=headers, **kwargs)
                if response.status_code in [429, 503] and attempt < retries:
                    backoff = (2 ** attempt) + random.uniform(0.5, 1.5)
                    await asyncio.sleep(backoff)
                    continue
                return response
            except Exception as e:
                if attempt == retries:
                    raise e
                await asyncio.sleep(1.0)

    async def close(self):
        await self.session.close()
