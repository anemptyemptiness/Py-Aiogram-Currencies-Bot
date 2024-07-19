import json
import pprint

from aiogram import Bot
from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

from bot.db.dao import RedisDAO
from bot.services.auto_request.publisher import auto_req_publisher


class AutoRequestConsumer:
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            bot: Bot,
            subject: str,
            stream: str,
            durable_name: str,
    ) -> None:
        self.nc = nc
        self.js = js
        self.bot = bot
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name

    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            manual_ack=True,
        )

    async def on_message(self, msg: Msg) -> None:
        currencies = dict()

        msg.headers.update(is_first_time=json.dumps(False))

        for key, value in msg.headers.items():
            currencies[key] = json.loads(value)

        msg.headers = dict()

        await RedisDAO.update_currencies(data=currencies)
        await msg.ack()

        # Публикуем новые валюты раз в сутки
        await auto_req_publisher(
            js=self.js,
            subject=self.subject,
            is_processed=True,
        )
