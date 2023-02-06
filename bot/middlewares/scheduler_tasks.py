import datetime

from aiogram import types

from config.settings import MEDIA_ROOT
from bot.middlewares.config import bot
from bot.middlewares import api


async def congratulation():
    """
    :return: None

    Function helps to send congratulations exact time to groups and users
    """
    data = api.get(addr=api.birthday)
    for birthday in data:
        await send_user_group(**birthday)
        # idx, name, image_path, congrat,date, user_id, groups = birthday.values()
        # await send_group(date, name, congrat, image_path, groups)
        # await send_user(name, congrat, image_path, user_id)


async def send_user_group(**kwargs):
    if checking_birthday(kwargs['date']):
        await send_group(**kwargs)
        await send_user(**kwargs)


async def send_group(date, name, congrat, image_id, groups, **kwargs):
    """
    :param congrat: str - congratulation
    :param name: str - name of birthday owner
    :param image_path:
    :param groups: List[int] - groups' id.
    :return: None
    """

    for group_id in groups:
        idx, chat_id, joined = api.get(group_id, api.group).values()
        if joined:
            await send_congrat(chat_id, name, congrat, image_id)


async def send_user(date, name, congrat, image_id, user, **kwargs):
    if user:
        userx = api.get(pk=user, addr=api.user)
        if userx['joined']:
            await send_congrat(userx['chat_id'], name, congrat, image_id)


async def send_congrat(chat_id, name, congrat, image_id):
    """
    :param chat_id:
    :param name:
    :param congrat:
    :param image_path:
    :return: None

    Function sends congratulation to groups or users
    """
    caption = f"🥳🥳🥳🥳🥳🥳🥳 Bugun biz uchun qadrdon bo`lgan {name}ning tug`ilgan kuni.\n{congrat}\n\n@{(await bot.get_me()).username}"
    try:
        await bot.send_photo(chat_id=chat_id, photo=image_id, caption=caption)
    except:
        await bot.send_message(chat_id=chat_id, text=caption)


def checking_birthday(date):
    """
    :param date:
    :return: Boolean

    Is birthday today? If yes, return True else False
    """
    birthdate = datetime.date.fromisoformat(date)
    today = datetime.date.today()
    if birthdate.month == today.month and birthdate.day == today.day:
        return True
    return False
