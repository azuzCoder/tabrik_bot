from aiogram import types
from config import dp, mongo_storage, bot

from postgresql import commands

table_name = "groups"


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def get_new_chat_member(message: types.Message):
    print(message)
    if message['new_chat_member']['id'] == bot.id:
        # data = await mongo_storage.get_data(user=bot.id)
        # groups = data.get('groups')
        # if groups is None:
        #     groups = []
        # groups.append({
        #     'chat_id': message.chat.id
        # })
        # data['groups'] = groups
        # await mongo_storage.set_data(user=bot.id, data=data)

        where = "WHERE chat_id=\'" + message.chat.id + "'"
        res = commands.select(table_name, ['id'], where)
        if len(res) > 0:
            id = res[0][0]


        fields = {
            'chat_id': message.chat.id,
            'joined': True
        }

        commands.insert(table_name, fields)


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

        fields = {
            ''
        }
