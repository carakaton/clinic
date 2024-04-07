import asyncio

from aiogram import Bot, Dispatcher

from app.make_an_appointment import router as make_an_appointment_router
from config import BOT_TOKEN


async def main():
    bot = Bot(BOT_TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_routers(make_an_appointment_router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
