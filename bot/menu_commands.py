from aiogram import types


async def set_default_commands(bot):
    await bot.set_my_commands([
        types.BotCommand(command="exchange", description="Обмен валюты"),
        types.BotCommand(command="rates", description="Список валют"),
    ])