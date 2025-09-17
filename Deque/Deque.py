from abc import ABC, abstractmethod
from typing import Final, Generic, List, TypeVar
from DynArray import DynArray

T = TypeVar("T")


class ParentQueue(Generic[T]):

    GET_HEAD_NIL: Final[int] = 0  # get_head() не выполнялась
    GET_HEAD_OK: Final[int] = 1  # get_head() завершилась успешно
    GET_HEAD_EMPTY: Final[int] = 2  # get_head() ошибка выполнения над пустым списком

    REMOVE_HEAD_NIL: Final[int] = 0  # remove_head() не выполнялась
    REMOVE_HEAD_OK: Final[int] = 1  # remove_head() завершилась успешно
    REMOVE_HEAD_EMPTY: Final[int] = (
        2  # remove_head() ошибка выполнения над пустым списком
    )

    # Постусловие: создана пустая очередь
    def __init__(self) -> None:
        self._array = DynArray()
        self._get_head_status: int = self.GET_HEAD_NIL
        self._remove_head_status: int = self.REMOVE_HEAD_NIL

    # Команды
    # Постусловие: добавляет элемент со значением value в хвост очереди
    def add_tail(self, value) -> None:
        self._array.append(value)

    # Предусловие: очередь не пуста
    # Постусловие: из очереди удален головной элемент
    def remove_head(self) -> None:
        if len(self._array) == 0:
            self._remove_head_status = self.REMOVE_HEAD_EMPTY
            raise IndexError("Index is out of bounds")
        self._remove_head_status = self.REMOVE_HEAD_OK
        self._array.remove(0)

    # Запросы
    # Предусловие: очередь не пуста
    def get_head(self) -> T:  # Возвращает значение в голове
        if len(self._array) == 0:
            self._get_head_status = self.GET_HEAD_EMPTY
            raise IndexError("Index is out of bounds")
        self._get_head_status = self.GET_HEAD_OK
        return self._array[0]

    def size(self) -> int:  # Возвращает размер очереди
        return len(self._array)

    # Запросы статусов
    # Возвращает значение REMOVE_HEAD_*
    def get_remove_head_status(self) -> int:
        return self._remove_head_status

    # Возвращает значение GET_HEAD_*
    def get_get_head_status(self) -> int:
        return self._get_head_status


class Deque(ParentQueue, Generic[T]):

    REMOVE_TAIL_NIL: Final[int] = 0  # remove_tail() не выполнялась
    REMOVE_TAIL_OK: Final[int] = 1  # remove_tail() завершилась успешно
    REMOVE_TAIL_EMPTY: Final[int] = (
        2  # remove_tail() ошибка выполнения над пустым списком
    )
    GET_TAIL_NIL: Final[int] = 0  # get_tail() не выполнялась
    GET_TAIL_OK: Final[int] = 1  # get_tail() завершилась успешно
    GET_TAIL_EMPTY: Final[int] = 2  # get_tail() ошибка выполнения над пустым списком

    def __init__(self):
        super().__init__()
        self._remove_tail_status: int = self.REMOVE_TAIL_NIL
        self._get_tail_status: int = self.GET_TAIL_NIL

    # Команды
    def add_head(self, value: T) -> None:
        self._array.insert(0, value)

    # Предусловие: очередь не пуста
    # Постусловие: из очереди удален хвостовой элемент
    def remove_tail(self) -> None:
        if len(self._array) == 0:
            self._remove_tail_status = self.REMOVE_TAIL_EMPTY
            raise IndexError("Index is out of bounds")
        self._array.remove(len(self._array) - 1)
        self._remove_tail_status = self.REMOVE_TAIL_OK

    # Запросы
    # Предусловие: очередь не пуста
    def get_tail(self) -> T:  # Возвращает занчение в хвосте
        if len(self._array) == 0:
            self._get_tail_status = self.GET_TAIL_EMPTY
            raise IndexError("Index is out of bounds")
        self._get_tail_status = self.GET_TAIL_OK
        return self._array[len(self._array) - 1]

    # Запросы статусов
    # Возвращает значение REMOVE_TAIL_*
    def get_remove_tail_status(self) -> int:
        return self._remove_tail_status

    # Возвращает значение GET_TAIL_*
    def get_get_tail_status(self) -> int:
        return self._get_tail_status
