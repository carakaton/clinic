from typing import Self


class Speciality:
    _specialities = {'Стоматолог', 'Дермотолог', 'Окулист'}

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    async def get_many(cls) -> list[Self]:
        return [cls(name) for name in cls._specialities]


class Doctor:
    _doctors = {'Иванов', 'Петров', 'Вылцан'}

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    async def get_many(cls, speciality: Speciality) -> list[Self]:
        return [cls(name) for name in cls._doctors]


class Date:
    _dates = {'Сегодня', 'Завтра', 'Послезавтра'}

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    async def get_many(cls, speciality, doctor) -> list[Self]:
        return [cls(name) for name in cls._dates]


class Time:
    _times = {'До обеда', 'В обед', 'После обеда'}

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    async def get_many(cls, speciality, doctor, date) -> list[Self]:
        return [cls(name) for name in cls._times]
