import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from aiogram import executor
from bot.middlewares.config import dp, scheduler
from bot.middlewares import scheduler_tasks

from bot.handlers import start_handler, birthday_handler, group_handler


if __name__ == '__main__':
    scheduler.add_job(func=scheduler_tasks.congratulation, trigger='cron', day_of_week='*', hour=0, minute=5)
    scheduler.start()
    executor.start_polling(skip_updates=True, dispatcher=dp)
