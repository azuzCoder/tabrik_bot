from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

BOT_API_TOKEN = '5505071713:AAHEq4b8BSycSzpumbKzm25H0_3XBjjyCPc'

bot = Bot(token=BOT_API_TOKEN)
mongo_storage = MongoStorage()
dp = Dispatcher(bot=bot, storage=mongo_storage)
