from .base import FakeModel
from .doctor_visiting import DoctorVisit


class Report(FakeModel):

    def __init__(self, visit: DoctorVisit, text: str):
        self.doctor = visit.doctor
        self.patient = visit.patient
        self.timestamp = visit.timestamp
        self.text = text
        super().__init__()

    def __str__(self):
        return f'{self.doctor.name} {self.doctor.speciality} заключил: {self.text}'
