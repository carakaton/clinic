from .base import FakeModel


class Patient(FakeModel):

    def __init__(self, tg_id: int, name: str, polis: int, age: int, sex: int):
        super().__init__()
        self.id = tg_id
        self.name = name
        self.age = age
        self.sex = sex
        self.polis = polis

    def __str__(self):
        return (
            f'Данные о пациенте\n'
            f'Имя: {self.name}\n'
            f'Возраст: {self.age}\n'
            f'Пол: {'Мужской' if self.sex == 1 else 'Женский'}\n'
            f'Полис: {self.polis}'
        )

    @property
    def is_old(self):
        return self.age >= 18

    @property
    def binary_sex_string(self):
        return 'Мужской' if self.sex == 1 else 'Женский'
