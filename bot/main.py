import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from aiogram import executor
from bot.middlewares.config import dp, scheduler
from bot.middlewares import scheduler_tasks

from bot.handlers import start_handler, group_handler
from bot.handlers.birthday import birthday_handler, list_birtdays

if __name__ == '__main__':
    scheduler.start()
    scheduler.remove_all_jobs()
    scheduler.pause()
    scheduler.add_job(func=scheduler_tasks.congratulation, trigger='cron', day_of_week='*', hour=0, minute=5)
    scheduler.resume()
    executor.start_polling(skip_updates=True, dispatcher=dp)
