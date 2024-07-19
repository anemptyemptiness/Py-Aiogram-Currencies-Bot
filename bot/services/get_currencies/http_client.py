from aiohttp import ClientSession


class CurrenciesClient:
    async def get_currencies(self, url: str) -> str:
        async with ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.text()
