import datetime

from aiogram import types

from config.settings import MEDIA_ROOT
from bot.middlewares.config import bot
from bot.middlewares import api


async def congratulation():
    data = api.list_birthdays()
    bot_data = await bot.get_me()
    for birthday in data:
        idx, name, image_path, congrat,date, user_id, groups = birthday.values()
        if checking_birthday(date):
            for group_id in groups:
                idx, chat_id, joiend = api.get_with_id_groups(group_id).values()
                if joiend:
                    await send_congrat(chat_id, name, date, congrat, image_path)
        if user_id:
            user = api.get_with_id_user(user_id)
            if user['joined']:
                await send_congrat(user['chat_id'], name, date, congrat, image_path)


async def send_congrat(chat_id, name, date, congrat, image_path):
    caption = f"🥳🥳🥳🥳🥳🥳🥳 Bugun biz uchun qadrdon bo`lgan {name}ning tug`ilgan kuni.\n{congrat}\n\n@{(await bot.get_me()).username}"
    await bot.send_photo(chat_id=chat_id, photo=types.InputFile(MEDIA_ROOT / image_path), caption=caption)


def checking_birthday(date):
    birthdate = datetime.date.fromisoformat(date)
    today = datetime.date.today()
    if birthdate.month == today.month and birthdate.day == today.day:
        return True
    return False
