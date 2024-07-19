from aiogram import Router
from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Group, Select, Back, Start, Row, Button
from aiogram_dialog.widgets.text import Format, Const

from bot.dialogs.getters import get_rates, get_rate
from bot.dialogs.handlers import rates_btn_clicked, move_left_handler, move_right_handler
from bot.fsm.fsm import RatesSG, StartSG

router = Router(name="router_rates")


rates_dialog = Dialog(
    Window(
        Const("Выберите валюту:"),
        Group(
            Select(
                Format("{item[0]}"),
                id="rates_btn",
                item_id_getter=lambda x: x[1],
                items="current_3_rates",
                on_click=rates_btn_clicked,
            ),
            width=1,
        ),
        Row(
            Button(
                text=Const("⬅️", when="can_move_left"),
                id="move_left_btn",
                on_click=move_left_handler,
            ),
            Button(
                text=Const("➡️", when="can_move_right"),
                id="move_right_btn",
                on_click=move_right_handler,
            ),
        ),
        Start(
            text=Const("Назад"),
            id="go_to_StartSG_menu_btn",
            state=StartSG.menu,
            mode=StartMode.RESET_STACK
        ),
        getter=get_rates,
        state=RatesSG.rates,
    ),
    Window(
        Const("Данные о выбранной валюте:\n"),
        Format("{rate_info}"),
        Back(
            text=Const("Назад"),
        ),
        getter=get_rate,
        state=RatesSG.rate,
    )
)

router.include_router(rates_dialog)
