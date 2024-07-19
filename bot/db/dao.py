import json
import logging
import pprint

from bot.config import redis

logger = logging.getLogger(__name__)


class RedisDAO:
    @classmethod
    async def update_currencies(
            cls,
            data: dict[str, dict],
    ) -> None:
        await redis.set("currencies", json.dumps(data))

    @classmethod
    async def get_currencies(cls) -> dict[str, dict]:
        return json.loads(await redis.get("currencies"))

    @classmethod
    async def get_currency(
            cls,
            currency_name: str,
    ) -> tuple[dict, str] | None:
        currency_name = currency_name.lower()

        try:
            currencies: dict[str, dict] = json.loads((await redis.get("currencies")).decode("utf-8"))

            if currencies.get(currency_name, None) is not None:
                return currencies.get(currency_name), currency_name
            return None
        except Exception as e:
            logger.exception(e)
