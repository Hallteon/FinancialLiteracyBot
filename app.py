import filters, middlewares, handlers
from aiogram import executor
from loader import dp
from utils import set_bot_commands
from utils.db_stuff.models import db, User


async def on_startup(dispatcher):
    await set_bot_commands.set_default_commands(dispatcher)
    db.connect()
    db.create_tables([User], safe=True)

    print('Бот включен!')


async def on_shutdown(dispatcher):
    db.close()
    print('Бот выключен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
