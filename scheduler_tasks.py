import datetime

from postgresql import commands


async def congrat():
    data = commands.select('birthdays', ['*'])
    for idx, full_name, description, date, file_path in data:
        today = datetime.date.today()
        birth_date = datetime.date.fromisoformat(date)

        if today.month == birth_date.month and today.day == birth_date.day:

