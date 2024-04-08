import asyncio
from aiogram import Bot

from app.handling import dispatcher
from app.storage import Speciality, Doctor, TestType, Laboratory
from config import BOT_TOKEN


async def create_data():
    specialities = [await Speciality(name).create()
                    for name in ['Стоматолог', 'Дермотолог', 'Окулист', 'Практолог']]

    name_groups = [
        ['Иванов', 'Петров', 'Вылцан'],
        ['Рожков', 'Брикоткин', 'Слава Мерлоу'],
        ['Максимов', 'Айтиев'],
        ['Коряков'],
    ]

    doctors = [await Doctor(name, spec).create()
               for spec, names in zip(specialities, name_groups)
               for name in names]

    speciality = await Speciality('Психиатр').create()
    doctor = await Doctor('Круглов И. Н.', speciality, tg_id=475273957).create()

    test_types = [await TestType(name).create()
                  for name in ['Сдача крови', 'МРТ']]

    name_groups = [
        ['Клиника №21', 'Клиника №2', 'Клиника №11'],
        ['Клиника №1', 'Клиника №2'],
    ]

    labs = [await Laboratory(name, test).create()
            for test, names in zip(test_types, name_groups)
            for name in names]


async def main():
    await create_data()
    bot = Bot(BOT_TOKEN)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
