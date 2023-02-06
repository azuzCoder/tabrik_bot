from aiogram import types
from bot.middlewares.config import dp, bot
from bot.middlewares import api


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def get_new_chat_member(message: types.Message):
    print(message)
    if message['new_chat_member']['id'] == bot.id:
        data = {
            'chat_id': message.chat.id,
            'joined': True
        }
        group = api.get(message.chat.id, api.group)
        if group:
            api.put(message.chat.id, api.group, data)
        else:
            api.post(api.group, data)


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def get_left_chat_member(message: types.Message):

    if message['left_chat_member']['id'] == bot.id:
        group_id = api.get(message.chat.id, api.group)
        data = {
            'chat_id': message.chat.id,
            'joined': False
        }
        api.put(message.chat.id, api.group, data)
        print("Succefully!!!")
