import asyncio
import logging
from aiogram import Bot, executor, Dispatcher, types

from config import BOT_TOKEN
from database import Database
from datetime import date


bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
db = Database("db.sqlite")


@dp.message_handler(commands=["start"])
async def start_handler(msg: types.Message):
    db.add_user(msg.from_user.id, msg.from_user.username)
    await msg.answer("Здарова, вот текущие цены на топляк.\nТеперь я буду автоматически присылать тебе новые цены, если они вдруг поменяются.")
    await send_price(msg.from_user.id)
    

async def send_price(user_id: int):
    cost_data = db.get_prices()
    text = format_message(cost_data)
    await bot.send_message(user_id, 
                           text)


def format_message(cost_data: dict) -> str:
    text = f"<b>Цены за литр на {date.today().strftime('%Y-%m-%d')}</b>\n\n"
    for item in sorted(cost_data.keys()):
        if cost_data[item]['compare'] == 1:
            compare = "🔺"
        elif cost_data[item]['compare'] == -1:
            compare = "🔻"
        else:
            compare = "➖"

        text += f"{item} -  {cost_data[item]['price']} ₽ {compare}\n"
    
    return text


async def send_changes():
    users = db.get_users()
    
    logging.info(f"Start sending notifactions") 
    for user in users:
        await send_price(user[0])
        logging.debug(f"Successfully sent to {user[0]}") 
        await asyncio.sleep(1)
    
    logging.info("Sending successfully completed")
    
        
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)