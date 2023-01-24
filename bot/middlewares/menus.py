from aiogram import types


async def main_menu():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add('Tug`ilgan kun qo`shish')

    return keyboard


async def remove_keyboard():
    return types.ReplyKeyboardRemove()
