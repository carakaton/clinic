from typing import Self, Iterable


class FakeModelMeta(type):

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        new_class._instances = {}
        new_class._counter = -1
        return new_class


class Many[T](list[T]):

    def __init__(self, objects: Iterable[T]):
        super().__init__(objects)

    def as_strs(self) -> list[str]:
        return list(map(str, self.copy()))

    def filter_one_by_str(self, string: str) -> T | None:
        found = [i for i in self if str(i) == string]
        return found[0] if found else None


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
    async def get_all(cls) -> Many[Self]:
        return Many(list(cls._instances.values()))

    @classmethod
    async def filter(cls, **filters) -> Many[Self]:
        return Many(i for i in cls._instances.values() if i._pass_filters(filters))

    def _pass_filters(self, filters):
        for key, value in filters.items():
            if self.__getattribute__(key) != value:
                return False
        return True
