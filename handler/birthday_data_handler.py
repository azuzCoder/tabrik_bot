from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import datetime

from config import bot, dp, mongo_storage
from states import Birthday
from postgresql import commands
import menus


@dp.message_handler(Text(equals='Tug`ilgan kun qo`shish', ignore_case=True))
async def input_birthday(message: types.Message):
    await Birthday.first()

    await message.answer('Ism familiyani kiriting\nMasalan: Aliyev Ali', reply_markup=await menus.remove_keyboard())


@dp.message_handler(state=Birthday.full_name, content_types=types.ContentType.ANY)
async def get_full_name(message: types.Message, state: FSMContext):

    if message.text:
        await state.update_data(full_name=message.text)
        await Birthday.next()

        await message.answer('Rasm jo`nating: ')
    else:
        await message.answer('Ism familiya noto`g`ri kiritildi!!!')


@dp.message_handler(state=Birthday.image, content_types=types.ContentType.PHOTO)
async def get_image(message: types.Message, state: FSMContext):
    if message.photo:
        await Birthday.next()
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id=file_id)
        await state.update_data(file_path=file.file_path)
        await file.download(destination_dir='../files/')

        await message.answer('Tarif kiriting: ')
    else:
        await message.answer("Rasm kiritilsin!!!")


@dp.message_handler(state=Birthday.description, content_types=types.ContentType.TEXT)
async def get_description(message: types.Message, state: FSMContext):
    if message.text:
        await Birthday.next()
        await state.update_data(description=message.text)

        await message.answer('Sana kiriting (kun.oy.yil)\nMasalan: 01.01.2000')
    else:
        await message.answer("Tarif noto`g`ri kiritildi!!!")


@dp.message_handler(state=Birthday.date, content_types=types.ContentType.TEXT)
async def get_date(message: types.Message, state: FSMContext):
    err = 'Sana noto`g`ri kiritildi!!!'
    if message.text:
        try:
            day, month, year = map(int, message.text.split('.'))
        except ValueError:
            await message.answer(err)
            return

        try:
            date = datetime.date(day=day, month=month, year=year)
        except ValueError:
            await message.answer(err)
            return

        await state.update_data(date=message.text)
        await Birthday.next()
        await send_list_groups(message=message)

    else:
        await message.answer(err)


async def send_list_groups(message: types.Message):
    groups = commands.select("groups", ['id', 'chat_id', 'joined'])
    buttons = types.InlineKeyboardMarkup()

    for idx, chat_id, joined in groups:
        admins = await bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == message.from_id:
                chat = await bot.get_chat(chat_id)
                buttons.add(types.InlineKeyboardButton(text=chat.title, callback_data=str(idx)))

    #
    # for groups_id in data:
    #     chat_id, joined = commands.select("groups", ['chat_id', 'joined'])[0]
    #     admins = await bot.get_chat_administrators(chat_id)
    #     for admin in admins:
    #         if admin.user.id == message.from_id and joined:
    #             chat = await bot.get_chat(chat_id)
    #             buttons.add(types.InlineKeyboardButton(text=chat.title, callback_data=chat_id))



    # # data = await mongo_storage.get_data(user=bot.id)
    # groups = data.get('groups')
    # if groups is None:
    #     groups = []
    # buttons = types.InlineKeyboardMarkup()
    # for group in groups:
    #     try:
    #         await bot.get_chat_member(chat_id=group['chat_id'], user_id=message.from_id)
    #     except ValueError:
    #         continue
    #     admins = await bot.get_chat_administrators(group['chat_id'])
    #     for admin in admins:
    #         if admin.user.id == message.from_id:
    #             chat = await bot.get_chat(group['chat_id'])
    #             buttons.add(types.InlineKeyboardButton(text=chat.title, callback_data=group['chat_id']))

    id = commands.select("users", ['id'], "WHERE chat_id=" + str(message.from_id))[0][0]
    buttons.add(types.InlineKeyboardButton(text='O`zim uchun', callback_data=str(id)))
    buttons.add(types.InlineKeyboardButton(text='Tugatish', callback_data='end'))
    await message.answer('Qayerga qo`shilsin? ', reply_markup=buttons)


@dp.callback_query_handler(Text(equals='end', ignore_case=True), state=Birthday.chat_list)
async def end_callback(callback: types.CallbackQuery, state: FSMContext):
    print(callback)





    # groups_list = callback.message.reply_markup.inline_keyboard
    # data = await state.get_data()
    # print(data)

    # if groups_list[-2][0].text.endswith('✅'):
    #     birthdays = data.get('birthdays')
    #     if not birthdays:
    #         birthdays = []
    #
    #     birthdays.append({
    #         'full_name': data['full_name'],
    #         'file_path': data['file_path'],
    #         'description': data['description'],
    #         'date': data['date']
    #     })
    #
    #     updated_data = {
    #         'birthdays': birthdays
    #     }
    #     await mongo_storage.set_data(user=callback.from_user.id, data=updated_data)
    #
    # for i in range(len(groups_list)-2):
    #     if groups_list[i][0].text.endswith('✅'):
    #         group_data = await mongo_storage.get_data(user=groups_list[i][0].callback_data)
    #         birthdays = group_data.get('birthdays')
    #         if not birthdays:
    #             birthdays = []
    #         birthdays.append({
    #             'full_name': data['full_name'],
    #             'date': data['date']
    #         })
    #         updated_data = {
    #             'bir
    #             thdays': birthdays
    #         }
    #         await mongo_storage.set_data(user=groups_list[i][0].callback_data, data=updated_data)

    await state.reset_state(with_data=False)

    await callback.message.delete_reply_markup()
    await callback.message.answer('Malumotlar saqlandi')
    from main import start
    await start(callback.message)


@dp.callback_query_handler(state=Birthday.chat_list)
async def edit_checked_button(callback: types.CallbackQuery, state: FSMContext):
    print(callback.message.reply_markup.inline_keyboard)
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



