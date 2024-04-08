from datetime import datetime
from .base import FakeModel


class Patient(FakeModel):

    def __init__(self, tg_id: int, polis: int):
        super().__init__()
        self.id = tg_id
        self.polis = polis

    def __str__(self):
        return (
            f'Данные о пациенте\n'
            f'Полис: {self.polis}'
        )
