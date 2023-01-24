import pytz

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

# apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

BOT_TOKEN = '5505071713:AAHEq4b8BSycSzpumbKzm25H0_3XBjjyCPc'

bot = Bot(token=BOT_TOKEN)
mongo_storage = MongoStorage()
dp = Dispatcher(bot=bot, storage=mongo_storage)

# APSCHEDULER configs
tz = pytz.timezone('Asia/Tashkent')

job_defaults = {
    "misfire_grace_time": 3600
}

jobstores = {
    "default": SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

scheduler = AsyncIOScheduler(
    timezone=tz,
    jobstores=jobstores,
    job_defaults=job_defaults
)
