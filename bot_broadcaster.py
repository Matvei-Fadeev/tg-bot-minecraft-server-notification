import pdb

import asyncio
import logging
import os
import datetime
import time
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor
from cfg import API_TOKEN, user_db_name, game_logs

# API_TOKEN = bot_token

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def get_ids_from_file():
    """
	Get ids of subscibed users from file

	:return: list of tg users id
    """
    users_ids = []
    with open(user_db_name, "r") as file:
        for line in file.readlines():
            users_ids.append(int(line))
    return users_ids


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender

    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster(text: str = "Empty", users_id: list = []) -> int:
    """
    Simple broadcaster

    :return: Count of messages
    """
    if not users_id:
        users_id = get_ids_from_file()

    print(users_id)
    print(text)

    count = 0
    try:
        for user_id in users_id:
            if await send_message(user_id, text):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count} messages successful sent.")

    return count


def send_message_by_ids(users_id: list, text: str):
	executor.start(dp, broadcaster(users_id, text))	


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def is_changed():
    """
    Return true when the log file will be changed
    """
    last_change = modification_date(game_logs)
    delay_between_check = 1 # in seconds
    while True:
        time.sleep(delay_between_check)
        current_last_change = modification_date(game_logs)
        if last_change != current_last_change:
            break
    return True


def get_text():
    last_line = ""
    with open(game_logs, "r") as f1:
        last_line = f1.readlines()[-1]
    if last_line.find("joined") != -1 or last_line.find("left") != -1:
        text = last_line.split("]: ")[1]   # '<b>${text}</b>'
        return text
    return ""


if __name__ == "__main__":
    # Infinite loop for every new connection
    while True:
        # wait for new connection
        if is_changed(): 
            text = get_text()                
            # if not empty then send message all saved users
            if text:      
                executor.start(dp, broadcaster(text))	
