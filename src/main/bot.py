import json

import messages as msgs

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
import os
from domain_parser import create_stats_table

REFRESH_TOKEN = os.getenv('refresh_token')
TOKEN = os.getenv('bot_token')
ADMINS = ["nikitosPy"]
DOMAIN = "habr.com"

bot = Bot(TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(msg: Message):
    if msg.from_user.username in ADMINS:
        await msg.answer(msgs.HELLO_MESSAGE.format(DOMAIN))

@dp.message_handler(commands=['get_stat'])
async def get_statistic(msg: Message):
    if msg.from_user.username in ADMINS:
        print(f'@{msg.from_user.username}')
        data = create_stats_table(REFRESH_TOKEN, DOMAIN)
        if not isinstance(data[0], type(None)):
            with open('result.xlsx', 'rb') as table_result:
                await msg.answer_document(table_result)

async def on_startup(dispatch: Dispatcher):
    print(f'ID: {dispatch.bot.id}')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
