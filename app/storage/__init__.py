from typing import Self, Sequence
from datetime import datetime


class FakeModelMeta(type):

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        new_class._instances = {}
        new_class._counter = -1
        return new_class


class FakeModel(metaclass=FakeModelMeta):

    _instances: dict[int, Self]

    def __init__(self, *args, **kwargs):
        self.id = self._get_new_id()

    @classmethod
    def _get_new_id(cls):
        cls._counter += 1
        return cls._counter

    async def create(self) -> Self:
        self._instances[self.id] = self
        return self

    @classmethod
    async def get_by_id(cls, id_: int) -> Self | None:
        return cls._instances.get(id_)

    @classmethod
    async def get_all(cls) -> Sequence[Self]:
        return list(cls._instances.values())

    @classmethod
    async def filter(cls, **filters) -> Sequence[Self]:
        return [i for i in cls._instances.values() if i._pass_filters(filters)]

    def _pass_filters(self, filters):
        for key, value in filters.items():
            if self.__getattribute__(key) != value:
                return False
        return True


class Patient(FakeModel):

    def __init__(self, tg_id: int, polis: int):
        super().__init__()
        self.id = tg_id
        self.polis = polis


class Appointment(FakeModel):

    def __init__(self, patient: 'Patient', doctor: 'Doctor', place: 'AppointmentPlace'):
        super().__init__()
        self.patient = patient
        self.doctor = doctor
        self.place = place
        self.place.is_busy = True

    def __str__(self):
        return f'{self.doctor.speciality.name} {self.doctor.name}, {self.place.date_string} в {self.place.time_string}'

    @classmethod
    async def get_all_for(cls, patient: Patient):
        return [i for i in cls._instances.values() if i.patient.id == patient.id]


class Speciality(FakeModel):

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name


class Doctor(FakeModel):

    def __init__(self, name: str, speciality: Speciality):
        super().__init__()
        self.name = name
        self.speciality = speciality

    def __str__(self):
        return self.name


class AppointmentPlace(FakeModel):

    def __init__(self, timestamp: datetime, doctor: Doctor):
        super().__init__()
        self.timestamp = timestamp
        self.doctor = doctor
        self.is_busy = False

    @property
    def date(self):
        return self.timestamp.date()

    @property
    def time(self):
        return self.timestamp.time()

    @classmethod
    async def get_not_busy_date_strings_for(cls, doctor):
        places = await AppointmentPlace.filter(doctor=doctor, is_busy=False)
        return [timestamp.strftime('%d.%m')
                for timestamp in sorted(list({place.date for place in places}))]

    @property
    def date_string(self):
        return self.timestamp.strftime('%d.%m')

    @property
    def time_string(self):
        return self.timestamp.strftime('%H:%M')
