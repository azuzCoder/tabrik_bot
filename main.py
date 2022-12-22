import pytz

import logging
import menus
import scheduler_tasks

from postgresql import commands
from psycopg2 import errors

from aiogram import executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import dp, scheduler


logging.basicConfig(level=logging.INFO)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*', content_types=types.ContentType.ANY)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.reset_state(with_data=False)

    await message.reply('Bekor qilindi.', reply_markup=types.ReplyKeyboardRemove())
    await start(message)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    print(message)

    try:
        commands.insert("users", {'chat_id': message.from_id})
    except errors.UniqueViolation:
        pass

    await message.answer(text='Asosiy sahifa', reply_markup=await menus.main_menu())
    # logging.info('start() is working!!!')


from handler import birthday_data_handler, join_left_handler


if __name__ == '__main__':
    scheduler.add_job(func=scheduler_tasks.congrat, trigger='cron', day_of_week='*', hour=15, minute=50)
    scheduler.start()
    executor.start_polling(dispatcher=dp, skip_updates=True)