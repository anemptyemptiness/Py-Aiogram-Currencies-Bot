import logging

from aiogram import Bot
from nats.aio.client import Client
from nats.js import JetStreamContext

from bot.services.auto_request.consumer import AutoRequestConsumer
from bot.services.auto_request.publisher import auto_req_publisher

logger = logging.getLogger(__name__)


async def start_auto_request_consumer(
        nc: Client,
        js: JetStreamContext,
        bot: Bot,
        subject: str,
        stream: str,
        durable_name: str,
) -> None:
    consumer = AutoRequestConsumer(
        nc=nc,
        js=js,
        bot=bot,
        subject=subject,
        stream=stream,
        durable_name=durable_name,
    )
    logger.info("Start auto_request consumer")
    await consumer.start()
    await auto_req_publisher(
        js=js,
        subject=subject,
    )
