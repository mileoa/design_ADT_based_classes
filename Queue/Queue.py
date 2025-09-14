from abc import ABC, abstractmethod
from typing import Final, Generic, List, TypeVar

T = TypeVar("T")


class QueueATD(ABC, Generic[T]):

    DEQUEUE_NIL: Final[int] = 0  # dequeue() не выполнялась
    DEQUEUE_OK: Final[int] = 1  # dequeue() завершилась успешно
    DEQUEUE_EMPTY: Final[int] = (
        2  # dequeue() ошибка выполнения над пустым списком
    )

    FIRST_NIL: Final[int] = 0  # first() не выполнялась
    FIRST_OK: Final[int] = 1  # first() завершилась успешно
    FIRST_EMPTY: Final[int] = 2  # first() ошибка выполнения над пустым списком

    # Постусловие: создана пустая очередь
    def __init__(self):
        pass

    # Команды
    @abstractmethod
    # Постусловие: добавляет элемент со значением value в конец очереди
    def enqueue(self, value: T) -> None:
        pass

    @abstractmethod
    # Предусловие: очередь не пуста
    # Постусловие: из очереди удален первый элемент
    def dequeue(self) -> None:
        pass

    # Запросы
    # Предусловие: очередь не пуста
    @abstractmethod
    def first(self) -> T:  # Возвращает первый элемент в очереди
        pass

    @abstractmethod
    def size(self) -> int:  # Возвращает размер очереди
        pass

    # Запросы статусов
    # Возвращает значение DEQUEUE_*
    @abstractmethod
    def get_dequeue_status(self) -> int:
        pass

    # Возвращает значение FIRST_*
    @abstractmethod
    def get_first_status(self) -> int:
        pass


class Queue(QueueATD, Generic[T]):
    def __init__(self) -> None:
        self._queue: List[T] = []
        self._begin: int = -1
        self._end: int = -1
        self._dequeue_status: int = self.DEQUEUE_NIL
        self._first_status: int = self.FIRST_NIL

    def enqueue(self, value: T) -> None:
        self._queue.append(value)
        self._end += 1

    def dequeue(self) -> None:
        if self._begin == self._end:
            self._dequeue_status = self.DEQUEUE_EMPTY
            raise IndexError("Queue is empty")
        self._begin += 1
        self._dequeue_status = self.DEQUEUE_OK

    def first(self) -> T:
        if self._begin == self._end:
            self._first_status = self.FIRST_EMPTY
            raise IndexError("Queue is empty")
        self._first_status = self.FIRST_OK
        return self._queue[self._begin + 1]

    def size(self) -> int:
        return self._end - self._begin

    def get_dequeue_status(self) -> int:
        return self._dequeue_status

    def get_first_status(self) -> int:
        return self._first_status
