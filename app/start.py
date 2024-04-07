import asyncio
from datetime import datetime
from aiogram import Bot

from app.handling import dispatcher
from app.storage import Speciality, Doctor, AppointmentPlace
from app.utils import get_14_days, get_8to20_times
from config import BOT_TOKEN


async def create_data():
    specialities = [await Speciality(name).create()
                    for name in ['Стоматолог', 'Дермотолог', 'Окулист']]

    name_groups = [
        ['Иванов', 'Петров', 'Вылцан'],
        ['Путин', 'Брикоткин', 'Слава Мерлоу'],
        ['Максимов', 'Айтиев', 'Коряков']
    ]

    doctors = [await Doctor(name, spec).create()
               for spec, names in zip(specialities, name_groups)
               for name in names]

    dates = [await AppointmentPlace(t, doc).create()
             for doc in doctors
             for day in get_14_days()
             for t in get_8to20_times(day)]

    # for date in dates:
    #     if date.timestamp < datetime.now():
    #         date.delete()


async def main():
    await create_data()
    bot = Bot(BOT_TOKEN)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
