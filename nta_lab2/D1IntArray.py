from typing import *


class D1IntArray(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __mod__(self, other: int):
        return self.map(lambda x: x % other)

    @staticmethod
    def _lencheck(a1, a2):
        if len(a1) != len(a2):
            raise ValueError("Arrays must be of equal length")

    @classmethod
    def zeros(cls, length: int):
        return cls([0] * length)

    @classmethod
    def full(cls, element, length):
        return cls([element] * length)

    @classmethod
    def multiply(cls, a1, a2, m: int | None = None):
        cls._lencheck(a1, a2)

        result = cls.zeros(len(a1))
        if m is None:
            for i in range(len(result)):
                result[i] = a1[i] * a2[i]
        else:
            for i in range(len(result)):
                result[i] = (a1[i] * a2[i]) % m

        return result

    @classmethod
    def power(cls, a1, a2, m: int | None = None):
        cls._lencheck(a1, a2)

        result = cls.zeros(len(a1))

        if m is None:
            for i in range(len(a1)):
                result[i] = pow(a1[i], a2[i])
        else:
            if m is None:
                for i in range(len(a1)):
                    result[i] = pow(a1[i], a2[i], m)

        return result

    def sum(self, m=None):
        if m is None:
            return sum(self)
        else:
            return sum(self) % m

    def prod(self, m=None):
        acc = 1
        if m is None:
            for e in self:
                acc *= e
        else:
            for e in self:
                acc = (acc * e) % m

        return acc

    def map(
        self,
        func: Callable[
            [
                int,
            ],
            int,
        ],
    ):
        result = D1IntArray.zeros(len(self))

        for i in range(len(self)):
            result[i] = func(self[i])

        return result
