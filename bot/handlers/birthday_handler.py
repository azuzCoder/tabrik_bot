from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import datetime

from config.settings import MEDIA_ROOT
from bot.middlewares.config import bot, dp
from bot.middlewares.states import Birthday
from bot.middlewares import menus, api


@dp.message_handler(Text(equals='Tug`ilgan kun qo`shish', ignore_case=True))
async def input_birthday(message: types.Message):
    await Birthday.first()

    await message.answer('Ism familiyani kiriting\nMasalan: Aliyev Ali', reply_markup=await menus.remove_keyboard())


@dp.message_handler(state=Birthday.name, content_types=types.ContentType.ANY)
async def get_full_name(message: types.Message, state: FSMContext):

    if message.text:
        await state.update_data(name=message.text)
        await Birthday.next()

        await message.answer('Rasm jo`nating: ')
    else:
        await message.answer('Ism familiya noto`g`ri kiritildi!!!')


@dp.message_handler(state=Birthday.image_path, content_types=types.ContentType.PHOTO)
async def get_image(message: types.Message, state: FSMContext):
    if message.photo:
        await Birthday.next()
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id=file_id)
        await file.download(destination_dir=MEDIA_ROOT)
        await state.update_data(image_path=file.file_path)

        await message.answer('Tarif kiriting: ')
    else:
        await message.answer("Rasm kiritilsin!!!")


@dp.message_handler(state=Birthday.congrat, content_types=types.ContentType.TEXT)
async def get_description(message: types.Message, state: FSMContext):
    if message.text:
        await Birthday.next()
        await state.update_data(congrat=message.text)

        await message.answer('Sana kiriting (yil.oy.kun)\nMasalan: 2000-01-01')
    else:
        await message.answer("Tarif noto`g`ri kiritildi!!!")


@dp.message_handler(state=Birthday.date, content_types=types.ContentType.TEXT)
async def get_date(message: types.Message, state: FSMContext):
    err = 'Sana noto`g`ri kiritildi!!!'
    if message.text:
        try:
            datetime.date.fromisoformat(message.text)
        except:
            await message.answer(err)
            return

        await state.update_data(date=message.text)
        await Birthday.next()
        await send_list_groups(message=message)

    else:
        await message.answer(err)


async def send_list_groups(message: types.Message):
    groups = api.list_groups()
    buttons = types.InlineKeyboardMarkup()

    for group in groups:
        idx, chat_id, joined = group.values()
        admins = await bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == message.from_id:
                chat = await bot.get_chat(chat_id)
                buttons.add(types.InlineKeyboardButton(text=chat.title, callback_data='g'+str(idx)))

    id = api.get_user(message.from_id)['id']
    buttons.add(types.InlineKeyboardButton(text='O`zim uchun', callback_data='u'+str(id)))
    buttons.add(types.InlineKeyboardButton(text='Tugatish', callback_data='end'))
    await message.answer('Qayerga qo`shilsin? ', reply_markup=buttons)


@dp.callback_query_handler(Text(equals='end', ignore_case=True), state=Birthday.chat_list)
async def end_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    groups_id = []
    inline_keyboard = callback.message.reply_markup.inline_keyboard
    for i in range(len(inline_keyboard)-2):
        for inline_button in inline_keyboard[i]:
            if inline_button.text.endswith('✅'):
                groups_id.append(int(inline_button.callback_data[1:]))

    myself = callback.message.reply_markup.inline_keyboard[-2][0]
    data['groups'] = groups_id
    if myself.text.endswith('✅'):
        # user_id = api.get_user(callback.from_user.id)['id']
        data['user'] = int(myself.callback_data[1:])

    api.add_birthday(data)
    await state.reset_state()

    await callback.message.delete_reply_markup()
    await callback.message.answer('Malumotlar saqlandi')
    from bot.handlers.start_handler import start
    await start(callback.message)


@dp.callback_query_handler(state=Birthday.chat_list)
async def edit_checked_button(callback: types.CallbackQuery, state: FSMContext):
    edited_keyboard = types.InlineKeyboardMarkup()
    for inline_button in callback.message.reply_markup.inline_keyboard:
        inline_button = inline_button[0]

        if inline_button.callback_data == callback.data:
            if inline_button.text.endswith('✅'):
                edited_keyboard.add(types.InlineKeyboardButton(
                    text=inline_button.text.rstrip('✅'),
                    callback_data=str(inline_button.callback_data)
                ))
            else:
                edited_keyboard.add(types.InlineKeyboardButton(
                    text=inline_button.text + '✅',
                    callback_data=str(inline_button.callback_data)
                ))
        else:
            edited_keyboard.add(types.InlineKeyboardButton(
                text=inline_button.text,
                callback_data=inline_button.callback_data)
            )
    await callback.message.edit_reply_markup(edited_keyboard)
