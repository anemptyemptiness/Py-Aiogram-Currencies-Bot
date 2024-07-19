import logging

from aiogram import Router
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput

from bot.dialogs.getters import get_exchange
from bot.dialogs.handlers import exchange_handler
from bot.fsm.fsm import ExchangeSG, StartSG

logger = logging.getLogger(__name__)
router = Router(name="router_exchange")


exchange_dialog = Dialog(
    Window(
        Const("Чтобы воспользоваться командой, следуй примеру:\n"),
        Const("<em>Пример: USD RUB 10</em>\n"),
        Const("Пояснение: <em>данная команда отображает стоимость 10 долларов в рублях</em>", when="no_data"),
        Format("\n✅ <b>{cur_from_nominal} {cur_from}</b> составляет <b>{exchange} {cur_to}</b>", when="exchange"),
        MessageInput(
            func=exchange_handler,
            content_types=ContentType.ANY,
        ),
        Start(
            text=Const("Назад"),
            id="go_to_StartSG_menu_btn",
            state=StartSG.menu,
            mode=StartMode.RESET_STACK,
        ),
        getter=get_exchange,
        state=ExchangeSG.exchange
    )
)

router.include_router(exchange_dialog)
