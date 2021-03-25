import logging
import os
import datetime
import time
import asyncio
from syncer import sync
import threading

from aiogram import Bot, Dispatcher, executor, types
from bot_token import bot_token

API_TOKEN = bot_token
user_db_name = "users_db"
game_logs = "/home/mine/nohup.out"
send_message_delay = 0.2
# online_users_nicknames = []

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()


def is_in_file(id):
    with open(user_db_name, "r") as file:
        s_id = str(id)
        for i in file:
            if i.strip() == s_id:
                print("\n\nGood\n\n")
                return True
    return False


def add_to_file(id):
    with open(user_db_name, "a") as file:
        file.write(str(id) + "\n")


def get_ids_from_file():
    users_ids = []
    with open(user_db_name, "r") as file:
        for line in file.readlines():
            users_ids.append(int(line))
    logging.debug(users_ids)
    return users_ids


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


@dp.message_handler()
async def message_handler(message: types.Message):
    mes = "Empty"
    user_id = message.from_user.id
    logging.debug(str(user_id))
    if not is_in_file(user_id):
        add_to_file(user_id)
        mes = "Add your to DB"
    else:
        mes = "Your already registered!"
    logging.debug(mes)

    await message.answer(mes)

@sync
async def send_text_to_user(id, text):
    await bot.send_message(id, text)

def send_text_to_user(id, text):
    bot.send_message(id, text).send

def send_updates_to_users(text):
    users_ids = get_ids_from_file()
    logging.debug(users_ids)
    for id in users_ids:
        send_text_to_user(id, text)
        logging.debug("ID: " + str(id) + " " + text)
        time.sleep(send_message_delay)


def check_updates():
    logging.debug("check_updates")
    last_change = modification_date(game_logs)
    while True:
        if last_change != modification_date(game_logs):
            logging.debug("last_change != modification_date(game_logs):")
            time.sleep(2)
            last_change = modification_date(game_logs)
            #os.system(f"tail -n 1 {game_logs}")
            last_line = ""
            with open(game_logs, "r") as f1:
                last_line = f1.readlines()[-1]
            logging.debug(last_line)
            if last_line.find("joined") != -1 or last_line.find("left") != -1:
                text = last_line.split("]: ")[1]
                send_updates_to_users(text)
                logging.debug("send_updates_to_users")


def main():
    t = threading.Thread(target=check_updates)
    t.start()
    #check_updates()
    #bot.send_message(1388600539, "Be 2 win")
    logging.debug("Beetween")
    #executor.start_polling(dp, skip_updates=True)
    executor.start_polling(dp)     


if __name__ == "__main__":
    main()
