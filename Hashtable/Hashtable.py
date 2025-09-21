import ctypes
from abc import ABC, abstractmethod
from typing import Final, Generic, List, TypeVar

T = TypeVar("T")


class HashtableATD(ABC, Generic[T]):

    PUT_NIL: Final[int] = 0  # put() не выполнялась
    PUT_OK: Final[int] = 1  # put() завершилась успешно
    PUT_ERR: Final[int] = (
        2  # put() завершилось с ошибкой, не удалось разрешить коллизию
    )

    REMOVE_NIL: Final[int] = 0  # remove() не выполнялась
    REMOVE_OK: Final[int] = 1  # remove() завершилась успешно
    REMOVE_NOT_FOUND: Final[int] = 2  # remove() не нашла элемент для удаления

    # Конструктор
    # Постусловие: создана пустая хэш-таблица
    def __init__(self, capacity: int):
        pass

    # Команды
    @abstractmethod
    # Предусловие: хеш-таблица не заполнена полностью
    # Постусловие: в таблицу добавлен элемент со значением value
    def put(self, value: T) -> None:
        pass

    @abstractmethod
    # Постусловие: из таблицы удален элемент со значением value
    def remove(self, value: T) -> None:
        pass

    # Запросы
    @abstractmethod
    # Возвращает результат проверки наличия элемента со значением
    #  value в хеш-таблице
    def contains(self, value: T) -> bool:
        pass

    @abstractmethod
    # Возвращает вместимость таблицы
    def get_capacity(self) -> int:
        pass

    @abstractmethod
    # Возвращает количество элементов в хеш-таблице
    def amount(self) -> int:
        pass

    # Запросы статусов
    @abstractmethod
    # Возвращает значение PUT_*
    def get_put_status(self) -> int:
        pass

    @abstractmethod
    # Возвращает значение REMOVE_*
    def get_remove_status(self) -> int:
        pass


class Hashtable(HashtableATD, Generic[T]):

    # Конструктор
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity of hashtable must be more than 0")
        self._CAPACITY: int = capacity
        self._slots: List[T | None] = [None] * self._CAPACITY
        self._amount: int = 0
        self._step: int = 3
        self._put_status: int = self.PUT_NIL
        self._remove_status: int = self.REMOVE_NIL

    # Команды
    def put(self, value: T) -> None:
        if self._amount == self._CAPACITY:
            self._put_status = self.PUT_ERR
            return
        index: int = self._seek_index_to_insert(value)
        if index == -1:
            self._put_status = self.PUT_ERR
            return
        self._slots[index] = value
        self._amount += 1
        self._put_status = self.PUT_OK

    def remove(self, value: T) -> None:
        index: int = self._seek_existing_index(value)
        if index == -1:
            self._remove_status = self.REMOVE_NOT_FOUND
            return
        self._slots[index] = None
        self._amount -= 1
        self._remove_status = self.REMOVE_OK

    # Запросы
    def contains(self, value: T) -> bool:
        index: int = self._seek_existing_index(value)
        return index != -1

    def amount(self) -> int:
        return self._amount

    def get_capacity(self):
        return self._CAPACITY

    # Запросы статусов
    def get_put_status(self) -> int:
        return self._put_status

    def get_remove_status(self) -> int:
        return self._remove_status

    # Функции для реализации
    def _hash_function(self, value: T) -> int:
        return hash(value) % self._CAPACITY

    def _seek_index_to_insert(self, value: T) -> int:
        hash: int = self._hash_function(value)
        index: int = hash
        attempt: int = 0
        current_step: int = self._get_step(attempt)

        while self._slots[index] is not None:
            index = (hash + current_step) % self._CAPACITY
            attempt += 1
            current_step = self._get_step(attempt)
            if index == hash:
                return -1
        return index

    def _seek_existing_index(self, value: T) -> int:
        hash: int = self._hash_function(value)
        index: int = hash
        attempt: int = 0
        current_step: int = self._get_step(attempt)

        while self._slots[index] is not None:
            index = (hash + current_step) % self._CAPACITY
            attempt += 1
            current_step = self._get_step(attempt)
            if self._slots[index] == value:
                return index
            if index == hash:
                return -1
        return -1

    def _get_step(self, attempt: int) -> int:
        return attempt * attempt
