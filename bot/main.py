import sys

sys.path.append('/home/azuz/PycharmProjects/django_project')

from aiogram import executor
from bot.middlewares.config import dp, scheduler
from bot.middlewares import scheduler_tasks

from bot.handlers import start_handler, birthday_handler, group_handler


if __name__ == '__main__':
    scheduler.add_job(func=scheduler_tasks.congratulation, trigger='cron', day_of_week='*', hour=23, minute=34)
    scheduler.start()
    executor.start_polling(skip_updates=True, dispatcher=dp)
