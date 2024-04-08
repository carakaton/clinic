from datetime import datetime

from .base import FakeModel
from .models import Patient


class TestType(FakeModel):

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name


class Laboratory(FakeModel):

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name


class Test(FakeModel):

    def __init__(self, laboratory: Laboratory, test_type: TestType):
        super().__init__()
        self.laboratory = laboratory
        self.type = test_type
        self.busy_visits: dict[datetime: TestVisit] = {}

    async def add_visit(self, patient: Patient, timestamp: datetime) -> None:
        visit = await TestVisit(patient, self, timestamp).create()
        self.busy_visits[visit.timestamp] = visit

    def __str__(self):
        return f'В {self.laboratory.name} {self.type.name}. Занятых мест: {len(list(self.busy_visits))}'


class TestVisit(FakeModel):

    def __init__(self, patient: Patient, test: Test, timestamp: datetime):
        super().__init__()
        self.patient = patient
        self.test = test
        self.timestamp = timestamp

    def __str__(self):
        str_timestamp = self.timestamp.strftime('%d.%m в %H:%M')
        return f'В {self.test.laboratory.name} {self.test.type.name} {str_timestamp}'
