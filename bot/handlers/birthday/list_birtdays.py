from datetime import date

from aiogram import types

from bot.middlewares.config import dp, bot
from bot.middlewares import api


@dp.message_handler(commands=['list_birthdays'])
async def list_birthdays(message: types.Message):
    birthdays = api.get(pk=message.chat.id, addr=api.get_or_update_user)['birthdays']
    print(birthdays)
    if len(birthdays) == 0:
        await message.answer('Sizda hali tug`ilgan kun qo`shilmagan.')
        return

    birthdays.sort(key=lambda s: (date.fromisoformat(s['date']).month, date.fromisoformat(s['date']).day))
    print(birthdays)

    text = ''
    curr = date.fromisoformat(birthdays[0]['date']).month
    text += month_name(curr) + ':' + '\n'
    for birthday in birthdays:
        birthdate = date.fromisoformat(birthday['date'])
        if curr != birthdate.month:
            curr = birthdate.month
            text += '\n' + month_name(curr) + ':' + '\n'
        text += '\t' + str(birthdate.day) + ' - ' + birthday['name'] + '\n'
    await message.answer(text=text)


def month_name(num: int):
    """
    This function return month name in UZBEK
    """

    if num == 1:
        return 'Yanvar'
    elif num == 2:
        return 'Fevral'
    elif num == 3:
        return 'Mart'
    elif num == 4:
        return 'Aprel'
    elif num == 5:
        return 'May'
    elif num == 6:
        return 'Iyun'
    elif num == 7:
        return 'Iyul'
    elif num == 8:
        return 'Avgust'
    elif num == 9:
        return 'Sentabr'
    elif num == 10:
        return 'Oktabr'
    elif num == 11:
        return 'Noyabr'
    elif num == 12:
        return 'Dekabr'
    else:
        return ''
