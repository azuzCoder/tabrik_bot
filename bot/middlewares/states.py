from aiogram.dispatcher.filters.state import State, StatesGroup


class Birthday(StatesGroup):
    name = State()
    image_path = State()
    congrat = State()
    date = State()
    chat_list = State()
