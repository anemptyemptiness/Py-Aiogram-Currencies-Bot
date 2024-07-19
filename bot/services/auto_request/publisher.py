import asyncio
import json

from nats.js import JetStreamContext

from bot.services.get_currencies.http_client import CurrenciesClient
from bot.services.parse_currencies.parser import Parser
from bot import settings


async def auto_req_publisher(
        js: JetStreamContext,
        subject: str,
        **kwargs,
) -> None:
    xml_text: str = await CurrenciesClient().get_currencies(url=settings.URL)
    currencies: list[dict[str, dict]] = Parser(xml_text=xml_text).parse()
    headers: dict = dict()

    for currency in currencies:
        for k, v in currency.items():
            headers[k.lower()] = json.dumps(v)

    if kwargs.get("is_processed", None) is None:
        # Парсим валюты первый раз
        await js.publish(subject=subject, headers=headers)
    else:
        # Парсим валюты раз в сутки
        await asyncio.sleep(60 * 60 * 24)
        await js.publish(subject=subject, headers=headers)
