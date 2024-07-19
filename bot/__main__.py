import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs

from bot.config import settings, redis
from bot.handlers import (
    router_startup,
    router_exchange,
    router_rates,
)
from bot.utils.connect_to_nats import connect_to_nats
from bot.utils.start_consumers import start_auto_request_consumer
from bot.menu_commands import set_default_commands


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        )
    )
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(storage=storage)

    # Подключаю роутеры
    dp.include_router(router_startup)
    dp.include_router(router_exchange)
    dp.include_router(router_rates)
    setup_dialogs(dp)

    nc, js = await connect_to_nats(servers=settings.NATS_HOST)

    logging.basicConfig(
        format='[{asctime}] #{levelname:8} {filename}: '
               '{lineno} - {name} - {message}',
        style="{",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)

    await set_default_commands(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await asyncio.gather(
            dp.start_polling(
                bot,
                js=js,
                subject=settings.NATS_CONSUMER_SUBJECT
            ),
            start_auto_request_consumer(
                nc=nc,
                js=js,
                bot=bot,
                subject=settings.NATS_CONSUMER_SUBJECT,
                stream=settings.NATS_STREAM,
                durable_name=settings.NATS_DURABLE_NAME
            )
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info("Connection to NATS closed")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    try:
        asyncio.run(main())
    except (Exception, KeyboardInterrupt):
        logger.info("Bot stopped")