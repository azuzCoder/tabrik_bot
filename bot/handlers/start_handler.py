from aiogram import types
from aiogram.types.bot_command_scope import BotCommandScopeChat
from aiogram.dispatcher import FSMContext
 
from bot.middlewares.config import dp, bot
from bot.middlewares import api, bot_commands


@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.reset_state()

    await message.reply('Bekor qilindi.', reply_markup=types.ReplyKeyboardRemove())
    await start(message)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    user = api.get(message.from_id, api.get_or_update_user)
    data = {
        'chat_id': message.from_id,
        'joined': True
    }
    if user:
        data['id'] = user['id']
        api.put(message.from_id, api.get_or_update_user, data)
    else:
        api.post(api.add_user, data)

    await bot.set_my_commands(commands=await bot_commands.main_commands(), scope=BotCommandScopeChat(message.chat.id))
    await message.answer(text='Asosiy sahifa')
