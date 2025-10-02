from abc import ABC, abstractmethod
from typing import Any, Dict, Final, Generic, TypeVar

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
    # Предусловие: элемент со значением value находится в массиве
    # Постусловие: из таблицы удален элемент со значением value
    def remove(self, value: T) -> None:
        pass

    # Запросы
    @abstractmethod
    # Возвращает результат проверки наличия элемента со значением
    #  value в хеш-таблице
    def contains(self, value: Any) -> bool:
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


class PowerSetATD(HashtableATD, Generic[T]):

    UNION_NIL: Final[int] = 0  # union() не выполнялась
    UNION_OK: Final[int] = 1  # union() успешно
    UNION_ERR_FULL: Final[int] = 2  # для union() не хватило вместимости

    DIFFER_NIL: Final[int] = 0  # differ() не выполнялась
    DIFFER_OK: Final[int] = 1  # differ() успешно
    DIFFER_ERR_FULL: Final[int] = 2  # для differ() не хватило вместимости

    # Команды
    @abstractmethod
    # Предусловие: таблица не заполнена полностью
    # Постусловие: если элемент не содержится в таблице,
    # то в таблицу добавлен элемент со значением value
    def put(self, value: T) -> None:
        pass

    # Постусловие: из текущего множества удалены все элементы,
    # которые не встречаются в переданном множестве
    @abstractmethod
    def intersect(self, power_set: "PowerSetATD") -> None:
        pass

    # Предусловие: количество уникальных элементов из текущего и
    # переданного множеств не превышает вместимость текущего множества
    # Постусловие: в текущее множество добавлены элементы переданного
    # множества, которые не содержатся в текущем множестве
    @abstractmethod
    def union(self, power_set: "PowerSetATD") -> None:
        pass

    # Предусловие: количество различающихся элементов между текущим и
    # переданным множеством не превышает вместимсоть текущего множества
    # Постусловие: из текущего множества удалены все элементы,
    # которые встречаются в переданном множестве и
    # добавлены элементы которые не встречаются
    @abstractmethod
    def differ(self, power_set: "PowerSetATD") -> None:
        pass

    # Запросы
    @abstractmethod
    # Возвращает количество совпадающих элементов
    # текущего множества и переданного
    def count_same(self, power_set: "PowerSetATD") -> int:
        pass

    @abstractmethod
    # Возвращает количество различающихся элементов
    # текущего множества и переданного
    def count_different(self, power_set: "PowerSetATD") -> int:
        pass

    # Запросы статусов
    @abstractmethod
    # Возвращает значение UNION_*
    def get_union_status(self) -> int:
        pass

    @abstractmethod
    # Возвращает значение DIFFER_*
    def get_differ_status(self) -> int:
        pass


class PowerSet(PowerSetATD, Generic[T]):

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be more than 0")
        self._CAPACITY: int = capacity
        self._slots: Dict[T, int] = {}
        self._amount: int = 0
        self._put_status: int = self.PUT_NIL
        self._remove_status: int = self.REMOVE_NIL
        self._union_status: int = self.UNION_NIL
        self._differ_status: int = self.DIFFER_NIL

    # Команды
    def put(self, value: T) -> None:
        if self._amount >= self._CAPACITY:
            self._put_status = self.PUT_ERR
            return
        if not self._slots.get(value) is not None:
            self._slots[value] = 0
            self._amount += 1
        self._put_status = self.PUT_OK

    def remove(self, value: T) -> None:
        if self._slots.get(value) is None:
            self._remove_status = self.REMOVE_NOT_FOUND
            return
        del self._slots[value]
        self._amount -= 1
        self._remove_status = self.REMOVE_OK

    def intersect(self, power_set: "PowerSetATD") -> None:
        slots_copy: Dict[T, int] = self._slots.copy()
        for element in slots_copy:
            if not power_set.contains(element):
                del self._slots[element]
                self._amount -= 1

    def union(self, power_set: "PowerSetATD") -> None:
        new_slots: Dict[T, int] = self._slots.copy()
        new_slots_amount: int = self._amount
        for element in power_set._slots:  # type: ignore[attr-defined]
            if new_slots.get(element) is None:
                new_slots[element] = 0
                new_slots_amount += 1
        if new_slots_amount > self._CAPACITY:
            self._union_status = self.UNION_ERR_FULL
            return
        self._slots = new_slots
        self._amount = new_slots_amount
        self._union_status = self.UNION_OK

    def differ(self, power_set: "PowerSetATD") -> None:
        new_slots: Dict[T, int] = self._slots.copy()
        new_slots_amount: int = self._amount
        for element in power_set._slots:  # type: ignore[attr-defined]
            if new_slots.get(element) is None:
                new_slots[element] = 0
                new_slots_amount += 1
                continue
            del new_slots[element]
            new_slots_amount -= 1
        if new_slots_amount > self._CAPACITY:
            self._differ_status = self.DIFFER_ERR_FULL
            return
        self._slots = new_slots
        self._amount = new_slots_amount
        self._differ_status = self.DIFFER_OK

    # Запросы
    def count_same(self, power_set: "PowerSetATD") -> int:
        same_elements_count: int = 0
        for element in self._slots:
            if power_set.contains(element):
                same_elements_count += 1
        return same_elements_count

    def count_different(self, power_set: "PowerSetATD") -> int:
        same_elements_count: int = 0
        for element in self._slots:
            if power_set.contains(element):
                same_elements_count += 1
        return self._amount + power_set.amount() - 2 * same_elements_count

    def contains(self, value: Any) -> bool:
        return self._slots.get(value) is not None

    def amount(self) -> int:
        return self._amount

    def get_capacity(self) -> int:
        return self._CAPACITY

    # Запросы статусов
    def get_put_status(self) -> int:
        return self._put_status

    def get_remove_status(self) -> int:
        return self._remove_status

    def get_union_status(self) -> int:
        return self._union_status

    def get_differ_status(self) -> int:
        return self._differ_status
