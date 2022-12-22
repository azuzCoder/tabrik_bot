import datetime

from postgresql import commands

from config import bot

from aiogram import types


async def congrat():
    data = commands.select('birthdays', ['*'])
    for idx, full_name, description, date, file_path in data:
        today = datetime.date.today()
        birth_date = date

        if today.month == birth_date.month and today.day == birth_date.day:
            birth_user = commands.select("birth_user", ['user_id'], "WHERE birth_id="+str(idx))
            for user_id, in birth_user:
                users = commands.select("users", ['chat_id'], "WHERE id=" + str(user_id))
                for chat_id, in users:
                    caption = f"{full_name}\n{description}\n{date}"
                    await bot.send_photo(chat_id=chat_id, photo=types.InputFile('files/'+file_path), caption=caption)
            birth_group = commands.select("birth_group", ['group_id'], "WHERE birth_id=" + str(idx))
            for group_id, in birth_group:
                groups = commands.select("groups", ['chat_id'], "WHERE id="+str(group_id) + " AND joined=true")
                for chat_id, in groups:
                    caption = f"{full_name}\n{description}\n{date}"
                    await bot.send_photo(chat_id=chat_id, photo=types.InputFile('files/'+file_path), caption=caption)
