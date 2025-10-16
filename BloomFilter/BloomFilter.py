import math
from abc import ABC
from random import randint
from typing import Any, Callable, Dict, Final, Generic, TypeVar

T = TypeVar("T")


class BloomFilterATD(ABC, Generic[T]):

    # Конструктор: создает фильтр Блюма для заданного
    # количества входных значений и требуемой точности
    def __init__(self, input_amount: int, accuracy_percent: float) -> None:
        pass

    # Команды
    # Постусловие: добавляет значение в фильтр
    def add(self, value: T) -> None:
        pass

    # Запросы
    # Возвращает результат проверки наличия значения в фильтре
    def is_value(self, value: T) -> bool:
        pass

    # Возвращает количество элементов на входе
    def get_input_amount(self) -> int:
        pass

    # Возвращает точность фильтра в процнетах
    def get_accuracy_percent(self) -> int:
        pass


class BloomFilter(BloomFilterATD, Generic[T]):

    # Конструктор
    def __init__(self, input_amount: int, accuracy_percent: float) -> None:
        if input_amount < 0:
            raise ValueError(
                f"input_amount должен быть > 0, получено: {input_amount}"
            )
        if accuracy_percent < 0.0 or accuracy_percent >= 99.99999999999999:
            raise ValueError(
                f"accuracy_percent должен быть < 99.99999999999999 и >= 0.0 получено: {accuracy_percent}"
            )
        self._input_amount: Final[int] = input_amount
        self._accuracy_percent = accuracy_percent
        self._bit_list: int = 0
        self._filter_size: int = self._caluclate_filter_size(
            self._input_amount, self._accuracy_percent
        )
        self._functions: list[Callable] = self._generate_hash_functions(
            self._caluclate_functions_amount(
                self._filter_size, self._input_amount
            )
        )

    # Команды
    def add(self, value: T) -> None:
        for function in self._functions:
            self._bit_list |= 1 << function(value)

    # Запросы
    def is_value(self, value: T) -> bool:
        mask: int = 0
        for function in self._functions:
            mask |= 1 << function(value)
        return mask & self._bit_list == mask

    def get_input_amount(self) -> int:
        return self._input_amount

    def get_accuracy_percent(self) -> int:
        return self._accuracy_percent

    # Функции для реализации
    def _generate_hash_functions(self, amount: int) -> list[Callable]:
        return [
            lambda value, seed=randint(1, self._filter_size): (
                hash(value) * seed
            )
            % self._filter_size
            for _ in range(amount)
        ]

    def _caluclate_filter_size(
        self, input_amount: int, accuracy_percent: float
    ) -> int:
        """
        Рассчитывает размер массива для заднной точности и
        количества входных элементов
        """
        false_positive_coefficient: float = 1 - accuracy_percent / 100
        return math.ceil(
            (input_amount * math.log(false_positive_coefficient))
            / math.log(1 / pow(2, math.log(2)))
        )

    def _caluclate_functions_amount(
        self, filter_size: int, input_amount: int
    ) -> int:
        """
        Рассчитывает количество функций для заднного
        разменра массива и количества элементов на входе
        """
        return round((filter_size / input_amount) * math.log(2))
