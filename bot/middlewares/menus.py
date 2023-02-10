from aiogram import types


async def main_menu():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add('Tug`ilgan kun qo`shish')

    return keyboard


async def remove_keyboard():
    return types.ReplyKeyboardRemove()


async def is_correct_menu():
    keyboards = types.InlineKeyboardMarkup()
    keyboards.add(types.InlineKeyboardButton('Ha', callback_data='yes'),
                  types.InlineKeyboardButton('Tahrirlash', callback_data='edit'),
                  types.InlineKeyboardButton('O`chirish', callback_data='delete'))
    return keyboards


def edit_menu():
    keyboard = types.InlineKeyboardMarkup()
    Inline = types.InlineKeyboardButton
    keyboard.add(Inline(text='Ism', callback_data='name'),
                 Inline(text='Rasm', callback_data='image_id'),
                 Inline(text='Tabrik', callback_data='congrat'),
                 Inline(text='Sana', callback_data='date'))
    keyboard.add(Inline(text='Davom etish...', callback_data='end'))

    return keyboard
