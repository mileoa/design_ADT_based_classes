# 2.2
# Операция tail не сводима к другим операциям при эффективной реализации, так как мы обладаем и понятием, и указателем на хвост.

# 2.3
# Операция поиска всех узлов не нужна, так как она сводится к уже существующим операциям head и циклическое выполение find, get пока статус find успешный или не выполнялся.

# 2.1
from abc import ABC, abstractmethod
from typing import Final, Generic, TypeVar

T = TypeVar("T")


class LinkedListATD(ABC, Generic[T]):

    HEAD_NIL: Final[int] = 0  # head() не выполнялась
    HEAD_OK: Final[int] = 1  # head() завершилась успешно
    HEAD_ERR: Final[int] = 2  # head() курсор не установлен

    TAIL_NIL: Final[int] = 0  # tail() не выполнялась
    TAIL_OK: Final[int] = 1  # tail() завершилась успешно
    TAIL_ERR: Final[int] = 2  # tail() курсор не установлен

    RIGHT_NIL: Final[int] = 0  # right() не выполнялась
    RIGHT_OK: Final[int] = 1  # right() завершилась успешно
    RIGHT_ERR_TAIL: Final[int] = 2  # right() курсор установлен на хвост
    RIGHT_ERR_EMPTY: Final[int] = 3  # right() курсор не установлен

    PUT_RIGHT_NIL: Final[int] = 0  # put_right() не выполнялась
    PUT_RIGHT_OK: Final[int] = 1  # put_right() завершилась успешно
    PUT_RIGHT_ERR_TAIL: Final[int] = 2  # put_right() курсор установлен на хвост
    PUT_RIGHT_ERR_EMPTY: Final[int] = 3  # put_right() курсор не установлен

    PUT_LEFT_NIL: Final[int] = 0  # put_left() не выполнялась
    PUT_LEFT_OK: Final[int] = 1  # put_left() завершилась успешно
    PUT_LEFT_ERR_HEAD: Final[int] = 2  # put_left() курсор установлен на голову
    PUT_LEFT_ERR_EMPTY: Final[int] = 3  # put_left() курсор не установлен

    REMOVE_NIL: Final[int] = 0  # remove() не выполнялась
    REMOVE_OK: Final[int] = 1  # remove() завершилась успешно
    REMOVE_ERR: Final[int] = 2  # remove() курсор не установлен

    ADD_TO_EMPTY_NIL: Final[int] = 0  # add_to_empty() не выполнялась
    ADD_TO_EMPTY_OK: Final[int] = 1  # add_to_empty() завершилась успешно
    ADD_TO_EMPTY_ERR: Final[int] = 2  # add_to_empty() курсор уже установлен

    ADD_TAIL_NIL: Final[int] = 0  # add_tail() не выполнялась
    ADD_TAIL_OK: Final[int] = 1  # add_tail() завершилась успешно
    ADD_TAIL_ERR: Final[int] = 2  # add_tail() курсор не установлен

    REPLACE_NIL: Final[int] = 0  # replace() не выполнялась
    REPLACE_OK: Final[int] = 1  # replace() завершилась успешно
    REPLACE_ERR: Final[int] = 2  # replace() курсор не установлен

    FIND_NIL: Final[int] = 0  # find() не выполнялась
    FIND_OK: Final[int] = 1  # find() завершилась успешно (значение найдено)
    # find() значение не найдено среди правых соседей
    FIND_ERR_NOT_FOUND: Final[int] = 2
    FIND_ERR_EMPTY: Final[int] = 3  # find() курсор не установлен

    GET_NIL: Final[int] = 0  # get() не выполнялась
    GET_OK: Final[int] = 1  # get() завершилась успешно
    GET_ERR: Final[int] = 2  # get() курсор не установлен

    # Конструктор
    # Постусловие: Создан связанный список с неустановленным курсором
    def __init__(self):
        pass

    # Команды
    # Предусловие: курсор установлен
    # Постусловие: курсор установлен на голову
    @abstractmethod
    def head() -> None:
        pass

    # Предусловие: курсор установлен
    # Постусловие: курсор установлен на хвост
    @abstractmethod
    def tail() -> None:
        pass

    # Предусловие: курсор установлен и курсор не на хвосте
    # Постусловие: новое значение добавлено в качестве левого соседа текущего
    # курсора и курсор установлен на новое значение
    @abstractmethod
    def right() -> None:
        pass

    # Предусловие: курсор установлен и курсор не в голове
    # Постусловие: новое значение добавлено в качестве правого
    # соседа текущего курсора и курсор установлен на новое значение
    @abstractmethod
    def put_right(self, value: T) -> None:
        pass

    # Предусловие: курсор установлен и курсор не на хвосте
    # Постусловие: курсор установлен на правого соседа
    @abstractmethod
    def put_left(self, value: T) -> None:
        pass

    # Предусловие: курсор установлен
    # Постусловие: курсор установлен на ближайшего соседа
    # начиная справа или не установлен
    @abstractmethod
    def remove(self) -> None:
        pass

    # Постусловие: курсор не установлен
    @abstractmethod
    def clear(self) -> None:
        pass

    # Предусловие: курсор не установлен
    # Постусловие: курсор установлен на указанное значение
    @abstractmethod
    def add_to_empty(self, value: T) -> None:
        pass

    # Предусловие: курсор установлен
    # Постусловие: новое значение установлено в качестве правого соседа хвоста
    @abstractmethod
    def add_tail(self, value: T) -> None:
        pass

    # Предусловие: курсор установлен
    # Постусловие: значение текущего курсора заменено на новое значение
    @abstractmethod
    def replace(self, value: T) -> None:
        pass

    # Предусловие: среди правых соседей текущего курсора есть искомое значение
    # Постусловие: курсор установлен на искомое значение
    # среде правых соседей текущего курсора
    @abstractmethod
    def find(self, value: T) -> None:
        pass

    # Постусловие: в списке не осталось указанного значения
    # и курсор установлен на значение отличное от искомого или не установлен
    @abstractmethod
    def remove_all(self, value: T) -> None:
        pass

    # Запросы
    # Предусловие: курсор установлен
    @abstractmethod
    def get(self) -> T:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def is_head(self) -> bool:
        pass

    @abstractmethod
    def is_tail(self) -> bool:
        pass

    @abstractmethod
    def is_value(self) -> bool:
        pass
