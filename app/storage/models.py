from datetime import datetime
from .base import FakeModel


class Patient(FakeModel):

    def __init__(self, tg_id: int, polis: int):
        super().__init__()
        self.id = tg_id
        self.polis = polis

    def __str__(self):
        return (
            f'Даныне о пациенте\n'
            f'Полис: {self.polis}'
        )


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


class TestType(Speciality):
    pass


class Doctor(FakeModel):

    def __init__(self, name: str, speciality: Speciality):
        super().__init__()
        self.name = name
        self.speciality = speciality

    def __str__(self):
        return self.name


class Laboratory(FakeModel):

    def __init__(self, name: str, test_type:TestType):
        super().__init__()
        self.name = name
        self.test_type = test_type

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


class Report(FakeModel):

    def __init__(self, patient: Patient, reporter: Doctor | Laboratory):
        super().__init__()
        self.for_patient = patient
        self.from_reporter = reporter
        self.timestamp = datetime.now()