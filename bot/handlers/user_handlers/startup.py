import logging

from aiogram import Router
from aiogram.filters.command import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const, Format

from bot.db.dao import RedisDAO
from bot.dialogs.getters import get_username
from bot.utils.paginate_rates import paginate_rates
from bot.fsm.fsm import StartSG, RatesSG, ExchangeSG

logger = logging.getLogger(__name__)
router = Router(name="router_startup")


menu_dialog = Dialog(
    Window(
        Format('👋 Здравствуй, <a href="{url}">{username}</a>!\n'),
        Const("/exchange - чтобы получить информацию о валюте"),
        Const("/rates - чтобы получить актуальные курсы валют"),
        getter=get_username,
        state=StartSG.menu,
    )
)


@router.message(CommandStart())
async def process_start_command(
        message: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(StartSG.menu, mode=StartMode.RESET_STACK)


@router.message(Command(commands=["rates"]))
async def process_rates_command(
        message: Message,
        dialog_manager: DialogManager,
) -> None:
    rates = await RedisDAO.get_currencies()
    rates.pop("is_first_time")

    paginate_rates.current_rates = rates
    paginate_rates.reset_all()

    await dialog_manager.start(RatesSG.rates, data={"current_3_rates": next(paginate_rates)})


@router.message(Command(commands="exchange"))
async def process_exchange_command(
        message: Message,
        dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(ExchangeSG.exchange)

router.include_router(menu_dialog)
