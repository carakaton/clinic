from datetime import datetime

from app.utils import get_next_14_work_days_timestamps
from .base import FakeModel, Many
from .patient import Patient
from .visit_datetime import VisitDate


class TestType(FakeModel):

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name


class Laboratory(FakeModel):

    def __init__(self, name: str, test_type: TestType):
        super().__init__()
        self.name = name
        self.test_type = test_type
        self.busy_visits: dict[datetime, TestVisit] = {}

    @staticmethod
    def get_free_visit_dates() -> Many[VisitDate]:
        dates = get_next_14_work_days_timestamps()
        return Many(VisitDate(d) for d in dates)

    async def add_visit(self, patient: Patient, timestamp: datetime) -> 'TestVisit':
        visit = await TestVisit(patient, self, timestamp).create()
        self.busy_visits[visit.timestamp] = visit
        return visit

    def __str__(self):
        return self.name


class TestVisit(FakeModel):

    def __init__(self, patient: Patient, laboratory: Laboratory, timestamp: datetime):
        super().__init__()
        self.patient = patient
        self.laboratory = laboratory
        self.timestamp = timestamp

    def __str__(self):
        str_timestamp = self.timestamp.strftime('%d.%m')
        return f'{self.laboratory.name} {self.laboratory.test_type.name} {str_timestamp}'
