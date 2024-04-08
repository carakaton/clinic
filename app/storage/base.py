from typing import Self, Sequence


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
