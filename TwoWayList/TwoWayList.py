from abc import ABC, abstractmethod
from typing import Final, Generic, Optional, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, v: T):
        self.value: T = v
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class ParentList(Generic[T]):

    HEAD_NIL: Final[int] = 0  # head() не выполнялась
    HEAD_OK: Final[int] = 1  # head() завершилась успешно
    HEAD_ERR_EMPTY: Final[int] = 2  # head() курсор не установлен

    TAIL_NIL: Final[int] = 0  # tail() не выполнялась
    TAIL_OK: Final[int] = 1  # tail() завершилась успешно
    TAIL_ERR_EMPTY: Final[int] = 2  # tail() курсор не установлен

    RIGHT_NIL: Final[int] = 0  # right() не выполнялась
    RIGHT_OK: Final[int] = 1  # right() завершилась успешно
    RIGHT_NO_ELEMENT: Final[int] = 2  # right() справа нет элемента

    PUT_RIGHT_NIL: Final[int] = 0  # put_right() не выполнялась
    PUT_RIGHT_OK: Final[int] = 1  # put_right() завершилась успешно
    PUT_RIGHT_ERR_EMPTY: Final[int] = 2  # put_right() список пуст

    PUT_LEFT_NIL: Final[int] = 0  # put_left() не выполнялась
    PUT_LEFT_OK: Final[int] = 1  # put_left() завершилась успешно
    PUT_LEFT_ERR_EMPTY: Final[int] = 2  # put_left() список пуст

    REMOVE_NIL: Final[int] = 0  # remove() не выполнялась
    REMOVE_OK: Final[int] = 1  # remove() завершилась успешно
    REMOVE_ERR_EMPTY: Final[int] = 2  # remove() курсор не установлен

    ADD_TO_EMPTY_NIL: Final[int] = 0  # add_to_empty() не выполнялась
    ADD_TO_EMPTY_OK: Final[int] = 1  # add_to_empty() завершилась успешно
    ADD_TO_EMPTY_ERR: Final[int] = 2  # add_to_empty() курсор уже установлен

    REPLACE_NIL: Final[int] = 0  # replace() не выполнялась
    REPLACE_OK: Final[int] = 1  # replace() завершилась успешно
    REPLACE_ERR_EMPTY: Final[int] = 2  # replace() курсор не установлен

    FIND_NIL: Final[int] = 0  # find() не выполнялась
    FIND_OK: Final[int] = 1  # find() завершилась успешно (значение найдено)
    # find() значение не найдено среди правых соседей
    FIND_ERR_NOT_FOUND: Final[int] = 2
    FIND_ERR_EMPTY: Final[int] = 3  # find() курсор не установлен

    GET_NIL: Final[int] = 0  # get() не выполнялась
    GET_OK: Final[int] = 1  # get() завершилась успешно
    GET_ERR_EMPTY: Final[int] = 2  # get() курсор не установлен

    # Конструктор
    # Постусловие: создан новый пустой список
    def __init__(self):
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._cursor: Optional[Node] = None
        self._size: int = 0
        self._set_statuses_to_nil()

    def _set_statuses_to_nil(self) -> None:
        self._head_status: int = self.HEAD_NIL
        self._tail_status: int = self.TAIL_NIL
        self._put_right_status: int = self.PUT_RIGHT_NIL
        self._put_left_status: int = self.PUT_LEFT_NIL
        self._remove_status: int = self.REMOVE_NIL
        self._add_to_emty_status: int = self.ADD_TO_EMPTY_NIL
        self._replace_status: int = self.REPLACE_NIL
        self._find_status: int = self.FIND_NIL
        self._get_status: int = self.GET_NIL
        self._right_status: int = self.RIGHT_NIL

    # Команды
    # Предусловие: список не пуст
    # Постусловие: курсор установлен на первый узел в списке
    def head(self) -> None:
        if self._size == 0:
            self._head_status = self.HEAD_ERR_EMPTY
            return None
        self._cursor = self._head
        self._head_status = self.HEAD_OK

    # Предусловие: список не пуст
    # Постусловие: курсор установлен на последний узел в списке
    def tail(self) -> None:
        if self._size == 0:
            self._tail_status = self.TAIL_ERR_EMPTY
            return None
        self._cursor = self._tail
        self._tail_status = self.TAIL_OK

    # Предусловие: правее курсора есть элемент
    # Постусловие: курсор сдвинут на один узел вправо
    def right(self) -> None:
        if self._size == 0:
            self._right_status = self.RIGHT_NO_ELEMENT
            return None
        if self._cursor is None:
            self._right_status = self.RIGHT_NO_ELEMENT
            return None
        if self._cursor.next is None:
            self._right_status = self.RIGHT_NO_ELEMENT
            return None
        self._cursor = self._cursor.next
        self._right_status = self.RIGHT_OK

    # Предусловие: список не пуст
    # Постусловие: следом за текущим узлом добавлен
    # новый узел с заданным значением
    def put_right(self, value: T) -> None:
        if self._size == 0:
            self._put_right_status = self.PUT_RIGHT_ERR_EMPTY
            return None
        new_node: Node = Node(value)
        new_node.next = self._cursor.next
        new_node.prev = self._cursor
        if self._cursor is self._tail:
            self._tail = new_node
        else:
            self._cursor.next.prev = new_node
        self._cursor.next = new_node
        self._size += 1
        self._put_right_status = self.PUT_RIGHT_OK
        return None

    # Предусловие: список не пуст
    # Постусловие: перед текущим узлом добавлен новый узел с заданным значением
    def put_left(self, value: T) -> None:
        if self._size == 0:
            self._put_left_status = self.PUT_LEFT_ERR_EMPTY
            return None
        new_node: Node = Node(value)
        new_node.next = self._cursor
        new_node.prev = self._cursor.prev
        if self._cursor is self._head:
            self._head = new_node
        else:
            self._cursor.prev.next = new_node
        self._cursor.prev = new_node
        self._size += 1
        self._put_left_status = self.PUT_LEFT_OK
        return None

    # Предусловие: список не пуст
    # Постусловие: текущий узел удалён, курсор смещён к правому соседу, если он есть,
    # в противном случае курсор смещён к левому соседу, если он есть
    def remove(self) -> None:
        if self._size == 0 or self._cursor is None:
            self._remove_status = self.REMOVE_ERR_EMPTY
            return None

        prev_node = self._cursor.prev
        next_node = self._cursor.next

        if prev_node:
            prev_node.next = next_node
        else:
            self._head = next_node

        if next_node:
            next_node.prev = prev_node
        else:
            self._tail = prev_node

        self._cursor.prev = None
        self._cursor.next = None

        if next_node:
            self._cursor = next_node
        elif prev_node:
            self._cursor = prev_node
        else:
            self._cursor = None

        self._size -= 1
        self._remove_status = self.REMOVE_OK
        return None

    # Постусловие: список очищен от всех элементов
    def clear(self) -> None:
        self._cursor = self._head
        node_to_delete: Optional[Node] = self._cursor
        while node_to_delete:
            self._head = node_to_delete.next
            node_to_delete.prev = None
            node_to_delete.next = None
            node_to_delete = self._head
            self._size -= 1
        self._tail = None
        self._cursor = None

        self._set_statuses_to_nil()
        return None

    # Предусловие: список пуст
    # Постусловие: в списке один узел
    def add_to_empty(self, value: T) -> None:
        if self._size > 0:
            self._add_to_emty_status = self.ADD_TO_EMPTY_ERR
            return None
        new_node: Node = Node(value)
        self._head = new_node
        self._tail = new_node
        self._cursor = new_node
        self._size += 1
        self._add_to_emty_status = self.ADD_TO_EMPTY_OK

    # Постусловие: новый узел добавлен в хвост списка
    def add_tail(self, value: T) -> None:
        if self._tail is None:
            self.add_to_empty(value)
            return None
        new_node: Node = Node(value)
        self._tail.next = new_node
        new_node.prev = self._tail
        self._tail = new_node
        self._size += 1

    # Предусловие: список не пуст
    # Постусловие: значение текущего узла заменено на новое
    def replace(self, value: T) -> None:
        if self._size == 0:
            self._replace_status = self.REPLACE_ERR_EMPTY
            return None
        self._cursor.value = value
        self._replace_status = self.REPLACE_OK

    # Постусловие: курсор установлен на следующий узел
    # с искомым значением, если такой узел найден
    def find(self, value: T) -> None:
        if self._size == 0:
            self._find_status = self.FIND_ERR_EMPTY
            return None
        find_cursor: Optional[Node] = self._cursor.next
        self._find_status = self.FIND_ERR_NOT_FOUND
        while find_cursor and self._find_status != self.FIND_OK:
            if find_cursor.value == value:
                self._cursor = find_cursor
                self._find_status = self.FIND_OK
            find_cursor = find_cursor.next
        return None

    # Постусловие: в списке удалены все узлы с заданным значением
    def remove_all(self, value: T) -> None:
        current = self._head
        while current:
            next_node = current.next
            if current.value != value:
                current = next_node
                continue

            if self._cursor is current and current.next:
                self._cursor = current.next
            if self._cursor is current and current.prev:
                self._cursor = current.prev
            if (
                self._cursor is current
                and not current.next
                and not current.prev
            ):
                self._cursor = None

            if current.prev:
                current.prev.next = current.next
            else:
                self._head = current.next

            if current.next:
                current.next.prev = current.prev
            else:
                self._tail = current.prev

            current.prev = None
            current.next = None

            self._size -= 1

            current = next_node

        return None

    # Запросы
    # Предусловие: список не пуст
    def get(self) -> T:
        if self._size == 0:
            self._get_status = self.GET_ERR_EMPTY
            raise ValueError(f"Курсор не установлен")
        self._get_status = self.GET_OK
        return self._cursor.value

    def size(self) -> int:
        return self._size

    def is_head(self) -> bool:
        return self._cursor and self._cursor is self._head

    def is_tail(self) -> bool:
        return self._cursor and self._cursor is self._tail

    def is_value(self) -> bool:
        return self._cursor is not None

    # Запросы статусов
    # Возвращает значение HEAD_*
    def get_head_status(self) -> int:
        return self._head_status

    # Возвращает значение TAIL_*
    def get_tail_status(self) -> int:
        return self._tail_status

    # Возвращает значение RIGHT_*
    def get_right_status(self) -> int:
        return self._right_status

    # Возвращает значение PUT_RIGHT_*
    def get_put_right_status(self) -> int:
        return self._put_right_status

    # Возвращает значение PUT_LEFT_*
    def get_put_left_status(self) -> int:
        return self._put_left_status

    # Возвращает значение REMOVE_*
    def get_remove_status(self) -> int:
        return self._remove_status

    # Возвращает значение ADD_TO_EMPTY_*
    def get_add_to_empty_status(self) -> int:
        return self._add_to_emty_status

    # Возвращает значение REPLACE_*
    def get_replace_status(self) -> int:
        return self._replace_status

    # Возвращает значение FIND_*
    def get_find_status(self) -> int:
        return self._find_status

    # Возвращает значение GET_*
    def get_get_status(self) -> int:
        return self._get_status


class LinkedList(ParentList, Generic[T]):
    pass


class TwoWayList(ParentList, Generic[T]):

    LEFT_NIL: Final[int] = 0  # left() не выполнялась
    LEFT_OK: Final[int] = 1  # left() завершилась успешно
    LEFT_NO_ELEMENT: Final[int] = 2  # left() слева нет элемента

    def __init__(self):
        super().__init__()
        self._set_statuses_to_nil()

    def _set_statuses_to_nil(self):
        super()._set_statuses_to_nil()
        self._left_status: int = self.LEFT_NIL

    # Команды
    # Предусловие: слева курсора есть элемент
    # Постусловие: курсор сдвинут на один узел влево
    def left(self) -> None:
        if self._size == 0:
            self._left_status = self.LEFT_NO_ELEMENT
            return None
        if self._cursor is None:
            self._left_status = self.LEFT_NO_ELEMENT
            return None
        if self._cursor.prev is None:
            self._left_status = self.LEFT_NO_ELEMENT
            return None
        self._cursor = self._cursor.prev
        self._left_status = self.LEFT_OK

    # Запросы статусов
    # Возвращает значение LEFT_*
    def get_left_status(self) -> int:
        return self._left_status
