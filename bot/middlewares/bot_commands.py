from aiogram.types import BotCommand


async def main_commands():
    commands = [BotCommand('add_birthday', 'Yangi tug`ilgan kun kiritish'),
                BotCommand('list_birthdays', 'Tug`ilgan kunlar ro`yhati')]

    return commands


async def cancel():
    commands = [BotCommand('cancel', 'Kiritishni bekor qilish')]

    return commands
