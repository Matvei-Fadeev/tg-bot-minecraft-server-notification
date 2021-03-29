import logging
from aiogram import Bot, Dispatcher, executor, types
from bot_token import bot_token

from cfg import API_TOKEN, user_db_name


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def is_in_file(id):
    """
    Check the user_id in file

    :param user_id:
    :return
    """
    with open(user_db_name, "r") as file:
        s_id = str(id)
        for i in file:
            if i.strip() == s_id:
                print("\n\nGood\n\n")
                return True
    return False


def add_to_file(id):
    """
    Add the user id to the next line in file

    :param user_id:
    :return: 
    """
    with open(user_db_name, "a") as file:
        file.write(str(id) + "\n")


@dp.message_handler()
async def message_handler(message: types.Message):
    mes = "Empty"
    user_id = message.from_user.id
    if not is_in_file(user_id):
        add_to_file(user_id)
        mes = "You are subscribed. When someone joins the server you'll get notification!"
    else:
        mes = "You are already subscribed!"

    await message.answer(mes)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
