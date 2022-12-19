from aiogram import types
from config import dp, mongo_storage, bot

from postgresql import commands

groups = "groups"
users = "users"


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def get_new_chat_member(message: types.Message):
    print(message)
    if message['new_chat_member']['id'] == bot.id:
        where = "WHERE chat_id=" + str(message.chat.id)
        res = commands.select(groups, ['id'], where)
        if len(res) > 0:
            id = res[0][0]
            commands.update(groups, [("joined", True)], "WHERE id=" + str(id))
        else:
            commands.insert(groups, {"chat_id": message.chat.id, "joined": True})


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def get_left_chat_member(message: types.Message):
    print(message)
    if message['left_chat_member']['id'] == bot.id:
        where = "WHERE chat_id=" + str(message.chat.id)
        res = commands.select(groups, ['id'], where)
        id = res[0][0]
        commands.update(groups, [("joined", False)], "WHERE id=" + str(id))
        print("Succefully!!!")
