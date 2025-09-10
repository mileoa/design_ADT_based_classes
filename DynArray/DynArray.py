import ctypes
from abc import ABC, abstractmethod
from typing import Final, Generic, List, TypeVar

T = TypeVar("T")


class DynArrayATD(Generic[T]):

    SETITEM_NIL: Final[int] = 0  # __setitem__ не выполнялся
    SETITEM_OK: Final[int] = 1  # __setitem__ завершился успешно
    SETITEM_ERR_INDEX: Final[int] = (
        2  # __setitem__ индекс превышает длину массива
    )

    REMOVE_NIL: Final[int] = 0  # remove() не выполнялся
    REMOVE_OK: Final[int] = 1  # remove() завершился успешно
    REMOVE_ERR_INDEX: Final[int] = 2  # remove() индекс превышает длину массива

    INSERT_NIL: Final[int] = 0  # insert() не выполнялся
    INSERT_OK: Final[int] = 1  # insert() завершился успешно
    INSERT_ERR_INDEX: Final[int] = 2  # insert() индекс превышает длину массива

    GETITEM_NIL: Final[int] = 0  # __getitem__ не выполнялся
    GETITEM_OK: Final[int] = 1  # __getitem__ завершился успешно
    GETITEM_ERR_INDEX: Final[int] = (
        2  # __getitem__ элемент отсутствует в указанной позиции
    )

    # Конструктор
    # Постусловие: создан пустой динамический массив
    def __init__(self, min_capacity: int) -> None:
        pass

    # Команды
    # Предусловие: указанная позиция не превышает длинну массива
    # Постусловие: элемент в данной позиции заменен на новый
    @abstractmethod
    def __setitem__(self, index: int, value: T) -> None:
        pass

    # Постусловие: в конец массива добавлен элемент
    @abstractmethod
    def append(self, value: T) -> None:
        pass

    # Предусловие: указанная позиция не превышает длинну массива
    # Постусловие: элемент из данной позиции удален и все жлементы
    # после данной позиции смещены влево
    @abstractmethod
    def remove(self, index: int) -> None:
        pass

    # Постусловие: массив очищен
    @abstractmethod
    def clear(self) -> None:
        pass

    # Предусловие: указанная позиция не превышает длинну массива
    # Постусловие: в даную позицию добавлен новый элемент и все элементы
    # с данной позиции смещены вперед
    @abstractmethod
    def insert(self, index: int, value: T) -> None:
        pass

    # Запросы
    # Предусловие: указанная позиция не превышает длинну массива
    @abstractmethod
    def __getitem__(self, index: int) -> T:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def get_min_capacity(self) -> int:
        pass

    # Запросы статусов
    # Возвращает значение SETITEM_*
    @abstractmethod
    def get_setitem_status(self) -> int:
        pass

    # Возвращает значение REMOVE_*
    @abstractmethod
    def get_remove_status(self) -> int:
        pass

    # Возвращает значение INSERT_*
    @abstractmethod
    def get_insert_status(self) -> int:
        pass

    # Возвращает значение GETITEM_*
    @abstractmethod
    def get_getitem_status(self) -> int:
        pass


class DynArray(DynArrayATD, Generic[T]):

    # Конструктор
    def __init__(self, min_capacity: int = 16):
        self.MIN_CAPACITY: int = min_capacity
        self.length: int = 0
        self.capacity: int = self.MIN_CAPACITY
        self.array: List[T] = self._make_array(self.capacity)

        self._setitem_status: int = self.SETITEM_NIL
        self._remove_status: int = self.REMOVE_NIL
        self._insert_status: int = self.INSERT_NIL
        self._getitem_status: int = self.GETITEM_NIL

    # Команды
    def __setitem__(self, index: int, value: T) -> None:
        if index < 0 or index >= self.length:
            self._setitem_status = self.SETITEM_ERR_INDEX
            raise IndexError("Index is out of bounds")
        self.array[index] = value
        self._setitem_status = self.SETITEM_OK

    def append(self, value: T) -> None:
        if self.length == self.capacity:
            self._resize(2 * self.capacity)
        self.array[self.length] = value
        self.length += 1

    def remove(self, index: int) -> None:
        if index < 0 or index >= self.length:
            self._remove_status = self.REMOVE_ERR_INDEX
            raise IndexError("Index is out of bounds")
        for j in range(index, self.length - 1):
            self.array[j] = self.array[j + 1]
        self.length -= 1
        if self.length < 0.5 * self.capacity:
            new_capacity = max(int(self.capacity / 1.5), self.MIN_CAPACITY)
            self._resize(new_capacity)
        self._remove_status = self.REMOVE_OK

    def clear(self) -> None:
        self.length = 0
        self.capacity = self.MIN_CAPACITY
        self.array = self._make_array(self.capacity)

        self._setitem_status = self.SETITEM_NIL
        self._remove_status = self.REMOVE_NIL
        self._insert_status = self.INSERT_NIL
        self._getitem_status = self.GETITEM_NIL

    def insert(self, index: int, value: T) -> None:
        if index < 0 or index > self.length:
            self._insert_status = self.INSERT_ERR_INDEX
            raise IndexError("Index is out of bounds")
        if self.length == self.capacity:
            self._resize(2 * self.capacity)
        for j in range(self.length, index, -1):
            self.array[j] = self.array[j - 1]
        self.array[index] = value
        self.length += 1
        self._insert_status = self.INSERT_OK

    # Запросы
    def __getitem__(self, index: int) -> T:
        if index < 0 or index >= self.length:
            self._getitem_status = self.GETITEM_ERR_INDEX
            raise IndexError("Index is out of bounds")
        self._getitem_status = self.GETITEM_OK
        return self.array[index]

    def __len__(self):
        return self.length

    def get_min_capacity(self) -> int:
        return self.MIN_CAPACITY

    # Запросы статусов
    def get_setitem_status(self) -> int:
        return self._setitem_status

    def get_remove_status(self) -> int:
        return self._remove_status

    def get_insert_status(self) -> int:
        return self._insert_status

    def get_getitem_status(self) -> int:
        return self._getitem_status

    # Вспомогательный код
    def _make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def _resize(self, new_capacity):
        new_array = self._make_array(new_capacity)
        for i in range(self.length):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity
