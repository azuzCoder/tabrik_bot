from aiogram.dispatcher.filters.state import State, StatesGroup


class Birthday(StatesGroup):
    full_name = State()
    image = State()
    description = State()
    date = State()
    chat_list = State()
