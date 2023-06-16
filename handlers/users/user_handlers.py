from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from loader import dp, bot
from utils.db_stuff.models import User


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    bot_name = await dp.bot.get_me()
    user = message.from_user
    new_user = User.get_or_create(id=user.id, username=user.username)
    text = f"👋 <b>{user.username}, привет!\n@{bot_name.username} 🤖 - это бот, с помощью " \
           f"которого можно развивать свою финансовую грамотность 📝\n" \
           f"Введи / или отправь команду /help " \
           f"чтобы увидеть доступные команды этого бота ✅</b>"

    await message.answer(text)

    if type(new_user) != tuple:
        new_user.save()


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "Доступные команды бота ✏:\n" \
           "/test - запустить тест по финансовой грамотности"

    await message.answer(text)





