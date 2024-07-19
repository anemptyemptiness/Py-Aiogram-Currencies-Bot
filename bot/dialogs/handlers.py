import logging

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot.db.dao import RedisDAO
from bot.utils.paginate_rates import paginate_rates

logger = logging.getLogger(__name__)


async def rates_btn_clicked(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        rate_index: str,
) -> None:
    info: str = ""
    unique_index: int = 0

    await dialog_manager.next()

    if "is_first_time" in dialog_manager.dialog_data:
        dialog_manager.dialog_data.pop("is_first_time")

    currencies = dialog_manager.dialog_data.get("currencies")
    current_currencies = dialog_manager.start_data.get("current_3_rates")

    for current_currency_name, index in current_currencies:
        if index == int(rate_index):
            unique_index = current_currencies.index([current_currency_name, index])

    currency_name = current_currencies[unique_index][0]

    for currency_code, currency_data in currencies.items():
        if currency_data['name'] == currency_name:
            info += (f"💳<b>Валюта</b>: <em>{currency_data['name']}</em>\n"
                     f"📋<b>Символьный код валюты</b>:  <em>{currency_code.upper()}</em>\n"
                     f"📟<b>Числовой код валюты</b>: <em>{currency_data['num_code']}</em>\n\n"
                     f"За <b>{currency_data['nominal']} {currency_code.upper()}</b> получим <b>{currency_data['value']} RUB</b>\n"
                     f"За <b>1 {currency_code.upper()}</b> получим <b>{currency_data['vunit_rate']} RUB</b>\n\n")

            dialog_manager.dialog_data.update(rate_info=info)
            return


async def exchange_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data.update(exchange=None)
    dialog_manager.show_mode = ShowMode.NO_UPDATE

    if message.content_type != ContentType.TEXT:
        await message.answer(
            text="😔 Кажется, это не текстовое сообщение\n\n"
                 "Чтобы воспользоваться командой, следуй примеру:\n"
                 "<em>Пример: /exchange USD RUB 10</em>",
        )
    else:
        if len(message.text.split()) != 3:
            await message.answer(
                text="😔 Кажется, вы некорректно воспользовались командой\n\n"
                     "Вот пример: <em>/exchange USD RUB 10</em>\n",
            )
        else:
            cur_from, cur_to, cur_from_nominal = message.text.split()

            try:
                cur_data, cur_name = await RedisDAO.get_currency(currency_name=cur_from.lower())
                exchange = float(cur_data["vunit_rate"].replace(",", ".")) * int(cur_from_nominal)

                dialog_manager.dialog_data.update(
                    {
                        "cur_from_nominal": cur_from_nominal,
                        'cur_from': cur_from.upper(),
                        "cur_to": cur_to.upper(),
                        "exchange": exchange,
                    }
                )
            except Exception as e:
                await message.answer(
                    text="Указанной валюты не нашлось...\n"
                         "Пожалуйста, проверьте корректность введённых данных!"
                )
            finally:
                dialog_manager.show_mode = ShowMode.SEND


async def move_left_handler(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    if paginate_rates._part_index == 0:
        dialog_manager.dialog_data.update(can_move_left=False)
        dialog_manager.dialog_data.update(can_move_right=True)
    else:
        dialog_manager.dialog_data.update(can_move_right=True)

        previous_3_rates = dialog_manager.start_data.get("current_3_rates")
        paginate_rates._part_index -= 1
        current_3_rates = paginate_rates._parts[paginate_rates._part_index]

        if paginate_rates._part_index == 0:
            dialog_manager.dialog_data.update(can_move_left=False)

        dialog_manager.start_data.update(current_3_rates=current_3_rates)
        dialog_manager.start_data.update(previous_3_rates=previous_3_rates)


async def move_right_handler(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
) -> None:
    if paginate_rates._part_index == paginate_rates._part_last_index:
        dialog_manager.dialog_data.update(can_move_right=False)
        dialog_manager.dialog_data.update(can_move_left=True)
    else:
        dialog_manager.dialog_data.update(can_move_left=True)

        previous_3_rates = dialog_manager.start_data.get("current_3_rates")
        current_3_rates = next(paginate_rates)

        if paginate_rates._part_index == paginate_rates._part_last_index:
            dialog_manager.dialog_data.update(can_move_right=False)

        dialog_manager.start_data.update(current_3_rates=current_3_rates)
        dialog_manager.start_data.update(previous_3_rates=previous_3_rates)