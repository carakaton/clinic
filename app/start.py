import asyncio
from aiogram import Bot

from app.client import dispatcher as client_dispatcher
from app.doctor import dispatcher as doctor_dispatcher
from app.storage import Speciality, Doctor, TestType, Laboratory, Patient
from app.config import CLIENT_BOT_TOKEN, DOCTOR_BOT_TOKEN


async def adding_docs():
    data = {
        'Дерматолог': ['Золотов П. Н.', 'Горозов Н. А.'],
        'Гастроэнтеролог': ['Огарева П. К.'],
        'Инфекционист': ['Оршевский К. К.'],
        'Кардиолог': ['Иванов. П. П.'],
        'Невролог': ['Иванов М. З.', 'Петров В. А.', 'Вылцан К. В.'],
        'Отоларинголог': ['Началова А. У.'],
        'Офтальмолог': ['Слава Мерлоу', 'Беляева А. А.'],
        'Психиатр нарколог': ['Устинова А. А.'],
        'Психотерапевт': ['Маликова. К. Н.'],
        'Стоматолог терапевт': ['Чкалова З. З.', 'Айтиев Д. Н.'],
        'Травмотолог': ['Жуоква П. А.'],
        'Хирург': ['Юдин А. А.', 'Жижин А. К.', 'Денисова А. Н.'],
    }

    for spec_name in data:
        spec = await Speciality(spec_name, for_kids=False if spec_name == 'Хирург' else None).create()
        for doc_name in data[spec_name]:
            await Doctor(doc_name, spec).create()


async def adding_labs():

    data = {
        'Сдача крови': ['Клиника №21', 'Клиника №2', 'Клиника №11'],
        'МРТ': ['Клиника №1', 'Клиника №2'],
    }

    for test_name in data:
        spec = await TestType(test_name).create()
        for lab_name in data[test_name]:
            await Laboratory(lab_name, spec).create()


async def adding_special():

    spec_for_woman = await Speciality('Акушер-гинеколог', for_sex=0).create()
    await Doctor('Боброва', spec_for_woman).create()
    spec_for_man = await Speciality('Уролог', for_sex=1).create()
    await Doctor('Артомонова А. А.', spec_for_woman).create()
    spec_for_kids = await Speciality('Педиатр', for_kids=True).create()
    await Doctor('Чичиков А. В.', spec_for_kids).create()
    await Doctor('Петрушкин Г. Н.', spec_for_kids).create()
    spec_for_kids = await Speciality('Психиатр детский', for_kids=True).create()
    await Doctor('Гоголева П. А.', spec_for_kids).create()
    spec_for_kids = await Speciality('Детский хирург', for_kids=True).create()
    await Doctor('Астахова Н. З.', spec_for_kids).create()
    spec_for_olds = await Speciality('Терапевт', for_kids=False).create()
    await Doctor('Ленина. К. Н.', spec_for_kids).create()
    await Doctor('Обрамова. У. А.', spec_for_kids).create()

    speciality = await Speciality('Психиатр', for_kids=False).create()
    await Doctor('Круглов И. Н.', speciality, tg_id=475273957).create()
    await Doctor('Чечеткин С. А.', speciality, tg_id=396359672).create()

    await Patient(475273957, 'Илья', 1234123412340000, 21, 1).create()


async def main():

    await adding_docs()
    await adding_labs()
    await adding_special()

    client_bot = Bot(CLIENT_BOT_TOKEN)
    doctor_bot = Bot(DOCTOR_BOT_TOKEN)

    await asyncio.gather(
        client_dispatcher.start_polling(client_bot),
        doctor_dispatcher.start_polling(doctor_bot),
    )


if __name__ == '__main__':
    asyncio.run(main())
