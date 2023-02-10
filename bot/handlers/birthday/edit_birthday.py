import datetime

from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext

from bot.middlewares.config import dp
from bot.middlewares.states import EditBirthday
from bot.handlers.birthday import birthday_handler
from bot.middlewares import menus


@dp.callback_query_handler(state=EditBirthday.basic)
async def basic(callback: CallbackQuery, state: FSMContext):
    text = None
    if callback.data == 'end':
        await birthday_handler.send_list_groups(callback)
    elif callback.data == 'name':
        text = 'Ism kiriting: '
        await EditBirthday.name.set()
    elif callback.data == 'image_id':
        text = 'Rasm jo`nating: '
        await EditBirthday.image_id.set()
    elif callback.data == 'congrat':
        text = 'Tabrik so`z kiriting: '
        await EditBirthday.congrat.set()
    elif callback.data == 'date':
        text = 'Sanani kiriting: '
        await EditBirthday.date.set()

    if text:
        await callback.message.answer(text)
    await callback.message.delete_reply_markup()


@dp.message_handler(state=EditBirthday.name, content_types=ContentType.ANY)
async def edit_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Ism noto`g`ri kiritildi!!!')

    if not birthday_handler.is_name_correct(message.text):
        await message.answer('Ismda ishlatish mumkin bo`lmagan belgilar bor \n(/ ; : \\ = [] {}).')
        return
    await state.update_data(name=message.text.strip())
    await send_edit_menu(message)


@dp.message_handler(state=EditBirthday.image_id, content_types=ContentType.ANY)
async def edit_image(message: Message, state: FSMContext):
    if not (message.photo or message.document and message.document.mime_base == 'image'):
        await message.answer("Rasm kiritilsin!!!")

    await state.update_data(image_id=birthday_handler.get_file_id(message))
    await send_edit_menu(message)


@dp.message_handler(state=EditBirthday.congrat, content_types=ContentType.ANY)
async def edit_congrat(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Tabrik noto`g`ri kiritildi!!!")

    await state.update_data(congrat=message.text)
    await send_edit_menu(message)


@dp.message_handler(state=EditBirthday.date, content_types=ContentType.ANY)
async def get_date(message: Message, state: FSMContext):
    err = 'Sana noto`g`ri kiritildi!!!'
    if not (message.text and birthday_handler.is_date_correct(message.text)):
        await message.answer(err)

    await state.update_data(date=message.text)
    await send_edit_menu(message)


async def send_edit_menu(message: Message):
    await EditBirthday.basic.set()
    await message.answer(text='Nimani o`zgartirmoqchisiz?', reply_markup=menus.edit_menu())
