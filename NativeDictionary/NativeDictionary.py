import ctypes
from abc import ABC, abstractmethod
from typing import Final, Generic, List, TypeVar

T = TypeVar("T")


class NativeDictionaryATD(ABC, Generic[T]):

    PUT_NIL: Final[int] = 0  # put() не выполнялась
    PUT_OK: Final[int] = 1  # put() завершилась успешно
    PUT_ERR: Final[int] = (
        2  # put() завершилось с ошибкой, не удалось разрешить коллизию
    )

    REMOVE_NIL: Final[int] = 0  # remove() не выполнялась
    REMOVE_OK: Final[int] = 1  # remove() завершилась успешно
    REMOVE_NOT_FOUND: Final[int] = 2  # remove() не нашла элемент для удаления

    GET_NIL: Final[int] = 0  # get() не выполнялась
    GET_OK: Final[int] = 1  # get() завершилась успешно
    GET_NOT_FOUND: Final[int] = 2  # get() не нашла элемент

    # Конструктор
    # Постусловие: создан пустой словарь
    def __init__(self, capacity: int):
        pass

    # Команды
    @abstractmethod
    # Предусловие: словарь не заполнен полностью
    # Постусловие: в таблицу добавлен элемент с ключом key и значением value
    def put(self, key: str, value: T) -> None:
        pass

    @abstractmethod
    # Предусловие: в словаре имеется элемент с ключом key
    # Постусловие: из словаря удален элемент с ключом key
    def remove(self, key: str) -> None:
        pass

    # Запросы
    @abstractmethod
    # Возвращает результат проверки наличия элемента с ключом
    #  key в словаре
    def contains(self, key: str) -> bool:
        pass

    @abstractmethod
    # Предусловие: в словаре содержится элемент с ключом key
    # Возвращает значение для ключа key
    def get(self, key: str) -> T:
        pass

    @abstractmethod
    # Возвращает вместимость словаря
    def get_capacity(self) -> int:
        pass

    @abstractmethod
    # Возвращает количество элементов в словаре
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

    @abstractmethod
    # Возвращает значение GET_*
    def get_get_status(self) -> int:
        pass


class NativeDictionary(NativeDictionaryATD, Generic[T]):

    # Конструктор
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity of hashtable must be more than 0")
        self._CAPACITY: int = capacity
        self._keys: List[T | None] = [None] * self._CAPACITY
        self._values: List[T | None] = [None] * self._CAPACITY
        self._amount: int = 0
        self._step: int = 1
        self._put_status: int = self.PUT_NIL
        self._remove_status: int = self.REMOVE_NIL
        self._get_status: int = self.GET_NIL

    # Команды
    def put(self, key: str, value: T) -> None:
        index: int = self._seek_slot(key)
        if index == -1:
            self._put_status = self.PUT_ERR
            return
        if self._keys[index] is None:
            self._keys[index] = key
            self._amount += 1
        self._values[index] = value
        self._put_status = self.PUT_OK

    def remove(self, key: str) -> None:
        index: int = self._seek_slot(key)
        if index == -1:
            self._remove_status = self.REMOVE_NOT_FOUND
            return
        if self._keys[index] is None:
            self._remove_status = self.REMOVE_NOT_FOUND
            return
        self._keys[index] = None
        self._amount -= 1
        self._remove_status = self.REMOVE_OK

    # Запросы
    def get(self, key: str) -> T:
        supposed_index: int = self._seek_slot(key)
        if supposed_index == -1:
            self._get_status = self.GET_NOT_FOUND
            raise KeyError(f"KeyError: {key}")
        if self._keys[supposed_index] is None:
            self._get_status = self.GET_NOT_FOUND
            raise KeyError(f"KeyError: {key}")
        self._get_status = self.GET_OK
        return self._values[supposed_index]

    def contains(self, key: str) -> bool:
        index: int = self._seek_slot(key)
        if index == -1:
            return False
        return self._keys[index] == key

    def amount(self) -> int:
        return self._amount

    def get_capacity(self):
        return self._CAPACITY

    # Запросы статусов
    def get_put_status(self) -> int:
        return self._put_status

    def get_remove_status(self) -> int:
        return self._remove_status

    def get_get_status(self) -> int:
        return self._get_status

    # Функции для реализации
    def _hash_fun(self, key: str) -> int:
        a: int = 7
        b: int = 11
        p: int = 7127
        x: int = 0
        for char in key:
            x += ord(char)
        return ((a * x + b) % p) % self._CAPACITY

    def _seek_slot(self, key) -> int:
        hash: int = self._hash_fun(key)
        index: int = hash
        current_step: int = self._step

        while self._keys[index] is not None:
            if self._keys[index] == key:
                return index
            index = (hash + current_step) % self._CAPACITY
            current_step += self._step
            if index == hash:
                return -1
        return index
