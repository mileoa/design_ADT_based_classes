from abc import ABC, abstractmethod
from typing import Final


class BoundedStackATD[T](ABC):

    POP_NIL: Final[int] = 0  # pop() не выполнялась
    POP_OK: Final[int] = 1  # pop() завершилась успешно
    POP_ERR: Final[int] = 2  # pop() стек пуст

    PEEK_NIL: Final[int] = 0  # peek() не выполнялась
    PEEK_OK: Final[int] = 1  # peek() завершилась успешно
    PEEK_ERR: Final[int] = 2  # peek() стек пуст

    PUSH_NIL: Final[int] = 0  # push() не выполнялась
    PUSH_OK: Final[int] = 1  # push() завершилась успешно
    PUSH_ERR: Final[int] = 2  # достигнуто максимальное количество элементов

    # Предусловие: max_size > 0
    # Постусловие: создан новый пустой стек, который может вместить
    # не более max_size элементов
    def __init__(self, max_size: int):
        pass

    # Предусловие: в стеке меньше max_size элементов
    # Постусловие: в стек добавлено новое значение
    @abstractmethod
    def push(self, value: T) -> None:
        pass

    # Предусловие: стек не пуст
    # Постусловие: из стека удалено последнее добавленное значение
    @abstractmethod
    def pop(self) -> None:
        pass

    # Предусловие: стек не пуст
    @abstractmethod
    def peek(self) -> T:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    # Постусловие: из стека удалятся все значения
    @abstractmethod
    def clear(self) -> None:
        pass

    # Возвращает значение PUSH_*
    @abstractmethod
    def get_push_status(self) -> int:
        pass

    # Возвращает значение PEEK_*
    @abstractmethod
    def get_peek_status(self) -> int:
        pass

    # Возвращает значение POP_*
    @abstractmethod
    def get_pop_status(self) -> int:
        pass


class BoundedStack[T](BoundedStackATD[T]):

    def __init__(self, max_size: int = 32) -> None:
        if max_size <= 0:
            raise ValueError(f"max_size должен быть > 0, получено: {max_size}")
        self._max_size: int = max_size
        self._stack: list[T] = []
        self._peek_status: int = self.PEEK_NIL
        self._push_status: int = self.PUSH_NIL
        self._pop_status: int = self.POP_NIL

    def push(self, value: T) -> None:
        if self.size() == self._max_size:
            self._push_status = self.PUSH_ERR
        else:
            self._stack.append(value)
            self._push_status = self.PUSH_OK
        return None

    def pop(self) -> None:
        if self.size() == 0:
            self._pop_status = self.POP_ERR
        else:
            del self._stack[-1]
            self._pop_status = self.POP_OK
        return None

    def peek(self) -> T:
        if self.size() == 0:
            result: T = 0
            self._peek_status = self.PEEK_ERR
        else:
            result: T = self._stack[-1]
            self._peek_status = self.PEEK_OK
        return result

    def size(self) -> int:
        return len(self._stack)

    def clear(self) -> None:
        self._stack: list[T] = []

        self._peek_status: int = self.PEEK_NIL
        self._push_status: int = self.PUSH_NIL
        self._pop_status: int = self.POP_NIL

    def get_push_status(self) -> int:
        return self._push_status

    def get_peek_status(self) -> int:
        return self._peek_status

    def get_pop_status(self) -> int:
        return self._pop_status
