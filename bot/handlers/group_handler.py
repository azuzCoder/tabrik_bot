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
        group = api.get_group(message.chat.id)
        if group:
            api.update_group(data)
        else:
            api.add_group(data)


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def get_left_chat_member(message: types.Message):

    if message['left_chat_member']['id'] == bot.id:
        # where = "WHERE chat_id=" + str(message.chat.id)
        # res = commands.select(groups, ['id'], where)
        # id = res[0][0]
        # commands.update(groups, [("joined", False)], "WHERE id=" + str(id))
        group_id = api.get_group(message.chat.id)
        data = {
            'id': group_id,
            'chat_id': message.chat.id,
            'joined': False
        }
        api.update_group(data)
        print("Succefully!!!")
