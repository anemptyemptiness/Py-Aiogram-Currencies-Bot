from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.db.dao import RedisDAO
from bot.utils.paginate_rates import paginate_rates


async def get_username(
        event_from_user: User,
        dialog_manager: DialogManager,
        **kwargs,
) -> dict:
    username = event_from_user.username
    url = event_from_user.url

    return {
        "username": username,
        "url": url,
    }


async def get_rates(
        dialog_manager: DialogManager,
        **kwargs,
) -> dict:
    currencies = await RedisDAO.get_currencies()

    if "is_first_time" in dialog_manager.dialog_data:
        dialog_manager.dialog_data.pop("is_first_time")

    dialog_manager.dialog_data.update(currencies=currencies)

    current_3_rates = dialog_manager.start_data.get("current_3_rates", None)
    previous_3_rates = dialog_manager.start_data.get("previous_3_rates", None)

    can_move_right: bool = dialog_manager.dialog_data.get("can_move_right")
    can_move_left: bool = dialog_manager.dialog_data.get("can_move_left")

    if current_3_rates and paginate_rates._part_index != paginate_rates._part_last_index:
        can_move_right: bool = True

    if previous_3_rates and paginate_rates._part_index != 0:
        can_move_left: bool = True

    return {
        "current_3_rates": current_3_rates,
        "previous_3_rates": previous_3_rates,
        "can_move_left": can_move_left,
        "can_move_right": can_move_right,
    }


async def get_rate(
        dialog_manager: DialogManager,
        **kwargs,
) -> dict:
    rate_info = dialog_manager.dialog_data.get("rate_info")

    return {
        "rate_info": rate_info,
    }


async def get_exchange(
        dialog_manager: DialogManager,
        **kwargs,
) -> dict:
    no_data = True

    if dialog_manager.dialog_data.get("exchange", None) is not None:
        no_data = False

        cur_from_nominal = dialog_manager.dialog_data.get("cur_from_nominal")
        cur_from = dialog_manager.dialog_data.get("cur_from")
        cur_to = dialog_manager.dialog_data.get("cur_to")
        exchange = dialog_manager.dialog_data.get("exchange")

        return {
            "no_data": no_data,
            "cur_from_nominal": cur_from_nominal,
            "cur_from": cur_from,
            "cur_to": cur_to,
            "exchange": exchange,
        }
    else:
        return {
            "no_data": no_data,
            "exchange": None,
        }