import asyncio
import aioschedule as schedule
from aiogram import executor
from bot import dp, send_changes
from database import Database
from parse import get_cost
import logging
from pathlib import Path

db = Database(Path(Path(__file__).parent.resolve(), "db.sqlite"))

logging.basicConfig(level=logging.INFO)

async def check_price_updates():
    old_prices = db.get_prices()
    new_prices = get_cost()
    if not old_prices:
        for i in new_prices.keys():
            db.save_price(i, new_prices[i]["price"], 0)
        
        return

    changed = []
    for i in new_prices.keys():
        if old_prices[i]["price"] != new_prices[i]["price"]:
            changed.append(i)

            if new_prices[i]["price"] > old_prices[i]["price"]:
                new_prices[i]["compare"] = 1
            elif new_prices[i]["price"] < old_prices[i]["price"]:
                new_prices[i]["compare"] = -1

            db.save_price(i, new_prices[i]["price"], new_prices[i]["compare"])
            logging.info(f"Price on {new_prices[i]} has changed") 
    
    if changed:
        for i in old_prices.keys():
            if i not in changed:
                db.save_price(i, old_prices[i]["price"], 0)

        await send_changes()

async def scheduler():
    schedule.every().minute.do(check_price_updates)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(2)


async def on_startup(_):
    logging.info("Bot started")
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
