from .base import FakeModel


class Patient(FakeModel):

    def __init__(self, tg_id: int, name: str, polis: int):
        super().__init__()
        self.id = tg_id
        self.name = name
        self.polis = polis

    def __str__(self):
        return (
            f'Данные о пациенте\n'
            f'Имя: {self.name}'
            f'Полис: {self.polis}'
        )
