import types

from aiogram import types
from aiogram.types.bot_command_scope import BotCommandScopeChat
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import datetime

from bot.middlewares.config import bot, dp
from bot.middlewares.states import Birthday, EditBirthday
from bot.middlewares import menus
from bot.middlewares import api, bot_commands
from bot.middlewares.scheduler_tasks import send_user_group, send_congrat


@dp.message_handler(commands=['add_birthday'])
async def input_birthday(message: types.Message, edit: bool=False):
    await Birthday.name.set()
    if edit:
        await message.answer(text='Iltimos malumotlarni qayta kiriting: ')
    else:
        await message.answer(text='Sizdan tug`ilgan kun egasi haqida ma\'lumot kiritish so`raladi.')

    await bot.set_my_commands(commands=await bot_commands.cancel(), scope=BotCommandScopeChat(message.chat.id))
    await message.answer('Ism kiriting\nMasalan: Jasur')


@dp.message_handler(state=Birthday.name, content_types=types.ContentType.ANY)
async def get_name(message: types.Message, state: FSMContext):
    if message.text:
        if not is_name_correct(message.text):
            await message.answer('Ismda ishlatish mumkin bo`lmagan belgilar bor \n(/ ; : \\ = [] {}).')
            return
        await state.update_data(name=message.text.strip())
        await Birthday.image_id.set()

        await message.answer('Rasm jo`nating: ')
    else:
        await message.answer('Ism noto`g`ri kiritildi!!!')


def is_name_correct(name: str):
    for s in name:
        if s == '/' or s == ';' or s == ':' or s == '\\' or s == '=' or s == '[' or s == ']' or s == '{' or s == '}':
            return False
    return True


@dp.message_handler(state=Birthday.image_id, content_types=types.ContentType.ANY)
async def get_image(message: types.Message, state: FSMContext):
    if not (message.photo or message.document and message.document.mime_base == 'image'):
        await message.answer("Rasm kiritilsin!!!")

    await Birthday.congrat.set()
    await state.update_data(image_id=get_file_id(message))
    await message.answer('Tabrik so`zini kiriting kiriting: ')


@dp.message_handler(state=Birthday.congrat, content_types=types.ContentType.ANY)
async def get_congrat(message: types.Message, state: FSMContext):
    if message.text:
        await Birthday.date.set()
        await state.update_data(congrat=message.text)

        await message.answer('Tug`ilgan sana kiritilsin (yil.oy.kun)\nMasalan: 2000-01-01')
    else:
        await message.answer("Tabrik noto`g`ri kiritildi!!!")


@dp.message_handler(state=Birthday.date, content_types=types.ContentType.ANY)
async def get_date(message: types.Message, state: FSMContext):
    err = 'Sana noto`g`ri kiritildi!!!'
    if message.text and is_date_correct(message.text):
        await state.update_data(date=message.text)
        data = await state.get_data()
        await Birthday.is_correct.set()
        await send_congrat(chat_id=message.from_user.id, name=data['name'], congrat=data['congrat'], image_id=data['image_id'])

        await message.answer(text='Malumotlar to`g`rimi?', reply_markup=await menus.is_correct_menu())

    else:
        await message.answer(err)


@dp.callback_query_handler(state=Birthday.is_correct)
async def is_correct(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data
    if data == 'yes':
        await send_list_groups(callback=callback)
    elif data == 'delete':
        from bot.handlers.start_handler import cancel_handler
        await cancel_handler(callback.message, state)
    elif data == 'edit':
        await EditBirthday.basic.set()
        print(await state.get_state())
        await callback.message.answer(text='Nimani o`zgartirmoqchisiz?', reply_markup=menus.edit_menu())
    await callback.message.delete_reply_markup()


async def send_list_groups(callback: types.CallbackQuery):
    await Birthday.chat_list.set()
    groups = api.get(addr=api.group)
    buttons = types.InlineKeyboardMarkup()

    for group in groups:
        chat_id, joined = group.values()
        admins = await bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == callback.from_user.id:
                chat = await bot.get_chat(chat_id)
                buttons.add(types.InlineKeyboardButton(text=chat.title + ' (guruh)', callback_data='g' + str(chat_id)))

    buttons.add(types.InlineKeyboardButton(text='Menga', callback_data='u' + str(callback.from_user.id)))
    buttons.add(types.InlineKeyboardButton(text='Mal\'lumotlarni saqlash', callback_data='end'))
    await callback.message.answer('Tug`ilgan kun haqida qayerlarda ma\'lumot berilsin.', reply_markup=buttons)


@dp.callback_query_handler(Text(equals='end', ignore_case=True), state=Birthday.chat_list)
async def end_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    groups_id = []
    inline_keyboard = callback.message.reply_markup.inline_keyboard
    for i in range(len(inline_keyboard) - 2):
        for inline_button in inline_keyboard[i]:
            if inline_button.text.endswith('✅'):
                groups_id.append(int(inline_button.callback_data[1:]))

    myself = callback.message.reply_markup.inline_keyboard[-2][0]
    data['groups'] = groups_id
    if myself.text.endswith('✅'):
        data['user'] = int(myself.callback_data[1:])

    data = api.post(addr=api.birthday, data=data)
    await send_user_group(**data)
    await state.reset_state()

    await callback.message.delete_reply_markup()
    await callback.message.answer('Malumotlar saqlandi')
    from bot.handlers.start_handler import start
    await start(callback.message)


@dp.callback_query_handler(state=Birthday.chat_list)
async def edit_checked_button(callback: types.CallbackQuery):
    edited_keyboard = types.InlineKeyboardMarkup()
    for inline_button in callback.message.reply_markup.inline_keyboard:
        inline_button = inline_button[0]
        data = str(inline_button.callback_data)
        if inline_button.callback_data == callback.data:
            if inline_button.text.endswith('✅'):
                text = inline_button.text.rstrip('✅')
            else:
                text = inline_button.text + '✅'
        else:
            text = inline_button.text
        if text:
            edited_keyboard.add(types.InlineKeyboardButton(
                text=text,
                callback_data=data
            ))
    await callback.message.edit_reply_markup(edited_keyboard)


def get_file_id(message: types.Message):
    if message.photo:
        return message.photo[-1].file_id
    return message.document.file_id


def is_date_correct(date: str):
    try:
        datetime.date.fromisoformat(date)
        return True
    except:
        return False
