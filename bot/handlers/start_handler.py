from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
 
from bot.middlewares.config import dp
from bot.middlewares import menus, api


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*', content_types=types.ContentType.ANY)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.reset_state()

    await message.reply('Bekor qilindi.', reply_markup=types.ReplyKeyboardRemove())
    await start(message)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    user = api.get_user(message.from_id)
    data = {
        'chat_id': message.from_id,
        'joined': True
    }
    if user:
        data['id'] = user['id']
        api.update_user(data)
    else:
        api.add_user(data)

    await message.answer(text='Asosiy sahifa', reply_markup=await menus.main_menu())
