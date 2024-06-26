from datetime import datetime

from app.utils import get_next_14_work_days_timestamps, get_visit_timestamps_for_full_work_day
from .base import FakeModel, Many
from .patient import Patient
from .visit_datetime import VisitDate, VisitTime


class Speciality(FakeModel):

    def __init__(self, name: str, for_sex: int = None, for_kids: bool = None):
        super().__init__()
        self.name = name
        self.for_kids = for_kids
        self.for_sex = for_sex

    def __str__(self):
        return self.name


class Doctor(FakeModel):

    def __init__(self, name: str, speciality: Speciality, tg_id: int = None):
        super().__init__()
        if tg_id:
            self.id = tg_id
        self.name = name
        self.speciality = speciality
        self.busy_visits: dict[datetime, DoctorVisit] = {}

    def get_free_visit_dates(self) -> Many[VisitDate]:
        dates = get_next_14_work_days_timestamps()
        return Many(VisitDate(d) for d in dates if self.get_free_visit_times(d))

    def get_free_visit_times(self, date: datetime) -> Many[VisitTime]:
        timestamps = get_visit_timestamps_for_full_work_day(date)
        return Many(VisitTime(t) for t in timestamps if t not in self.busy_visits)

    async def add_visit(self, patient: Patient, timestamp: datetime) -> 'DoctorVisit':
        visit = await DoctorVisit(patient, self, timestamp).create()
        self.busy_visits[visit.timestamp] = visit
        return visit

    async def remove_visit(self, visit: 'DoctorVisit') -> None:
        del self.busy_visits[visit.timestamp]
        await visit.delete()

    def __str__(self):
        return self.name


class DoctorVisit(FakeModel):

    def __init__(self, patient: Patient, doctor: Doctor, timestamp: datetime):
        super().__init__()
        self.patient = patient
        self.doctor = doctor
        self.timestamp = timestamp

    def __str__(self):
        str_timestamp = self.timestamp.strftime('%d.%m в %H:%M')
        return f'{self.doctor.speciality.name} {self.doctor.name} {str_timestamp}'

    @classmethod
    async def get_all_for(cls, patient: Patient):
        return [i for i in cls._instances.values() if i.patient.id == patient.id]
