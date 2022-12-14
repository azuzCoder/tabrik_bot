from aiogram import types
from config import dp, mongo_storage, bot


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def get_new_chat_member(message: types.Message):
    print(message)
    if message['new_chat_member']['id'] == bot.id:
        data = await mongo_storage.get_data(user=bot.id)
        groups = data.get('groups')
        if groups is None:
            groups = []
        groups.append({
            'chat_id': message.chat.id
        })
        data['groups'] = groups
        await mongo_storage.set_data(user=bot.id, data=data)


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def get_left_chat_member(message: types.Message):
    print(message)
    if message['left_chat_member']['id'] == bot.id:
        data = await mongo_storage.get_data(user=bot.id)
        groups = data.get('groups')
        if groups is None:
            groups = []
        groups = list(filter(lambda a: True if a['chat_id'] != message.chat.id else False, groups))
        data['groups'] = groups
        await mongo_storage.set_data(user=bot.id, data=data)
