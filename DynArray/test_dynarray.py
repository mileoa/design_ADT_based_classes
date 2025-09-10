import unittest
from typing import Any

from DynArray import DynArray


class TestDynArray(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом."""
        self.array = DynArray[int](min_capacity=4)
        self.str_array = DynArray[str](min_capacity=2)

    def test_constructor(self):
        """Тест конструктора."""
        # Создание пустого массива
        arr = DynArray[int](min_capacity=10)
        self.assertEqual(len(arr), 0)
        self.assertEqual(arr.get_min_capacity(), 10)

        # Проверка начальных статусов
        self.assertEqual(arr.get_setitem_status(), DynArray.SETITEM_NIL)
        self.assertEqual(arr.get_remove_status(), DynArray.REMOVE_NIL)
        self.assertEqual(arr.get_insert_status(), DynArray.INSERT_NIL)
        self.assertEqual(arr.get_getitem_status(), DynArray.GETITEM_NIL)

    def test_append(self):
        """Тест добавления элементов в конец массива."""
        # Добавление элементов
        self.array.append(10)
        self.assertEqual(len(self.array), 1)
        self.array.append(20)
        self.array.append(30)
        self.assertEqual(len(self.array), 3)

        # Проверка содержимого
        self.assertEqual(self.array[0], 10)
        self.assertEqual(self.array[1], 20)
        self.assertEqual(self.array[2], 30)

    def test_setitem_success(self):
        """Тест успешной установки элемента по индексу."""
        # Подготовка массива
        self.array.append(1)
        self.array.append(2)
        self.array.append(3)

        # Успешная установка существующего элемента
        self.array[1] = 99
        self.assertEqual(self.array[1], 99)
        self.assertEqual(self.array.get_setitem_status(), DynArray.SETITEM_OK)

        # Установка первого элемента
        self.array[0] = 88
        self.assertEqual(self.array[0], 88)
        self.assertEqual(self.array.get_setitem_status(), DynArray.SETITEM_OK)

        # Установка последнего элемента
        self.array[2] = 77
        self.assertEqual(self.array[2], 77)
        self.assertEqual(self.array.get_setitem_status(), DynArray.SETITEM_OK)

    def test_setitem_index_error(self):
        """Тест исключения при выходе индекса за пределы массива в setitem."""
        # Пустой массив
        with self.assertRaises(IndexError):
            self.array[0] = 10
        self.assertEqual(
            self.array.get_setitem_status(), DynArray.SETITEM_ERR_INDEX
        )

        # Массив с элементами
        self.array.append(1)
        self.array.append(2)

        # Индекс больше длины
        with self.assertRaises(IndexError):
            self.array[5] = 100
        self.assertEqual(
            self.array.get_setitem_status(), DynArray.SETITEM_ERR_INDEX
        )

        # Отрицательный индекс больше длины
        with self.assertRaises(IndexError):
            self.array[-10] = 100
        self.assertEqual(
            self.array.get_setitem_status(), DynArray.SETITEM_ERR_INDEX
        )

    def test_getitem_success(self):
        """Тест успешного получения элемента по индексу."""
        # Подготовка данных
        self.array.append(100)
        self.array.append(200)
        self.array.append(300)

        # Получение элементов
        self.assertEqual(self.array[0], 100)
        self.assertEqual(self.array.get_getitem_status(), DynArray.GETITEM_OK)

        self.assertEqual(self.array[1], 200)
        self.assertEqual(self.array.get_getitem_status(), DynArray.GETITEM_OK)

        self.assertEqual(self.array[2], 300)
        self.assertEqual(self.array.get_getitem_status(), DynArray.GETITEM_OK)

    def test_getitem_index_error(self):
        """Тест исключения при выходе индекса за пределы массива в getitem."""
        # Пустой массив
        with self.assertRaises(IndexError):
            _ = self.array[0]
        self.assertEqual(
            self.array.get_getitem_status(), DynArray.GETITEM_ERR_INDEX
        )

        # Массив с элементами
        self.array.append(1)
        self.array.append(2)

        # Индекс больше длины
        with self.assertRaises(IndexError):
            _ = self.array[5]
        self.assertEqual(
            self.array.get_getitem_status(), DynArray.GETITEM_ERR_INDEX
        )

        # Отрицательный индекс больше длины
        with self.assertRaises(IndexError):
            _ = self.array[-10]
        self.assertEqual(
            self.array.get_getitem_status(), DynArray.GETITEM_ERR_INDEX
        )

    def test_remove_success(self):
        """Тест успешного удаления элемента."""
        # Подготовка данных
        self.array.append(10)
        self.array.append(20)
        self.array.append(30)
        self.array.append(40)

        # Удаление из середины
        self.array.remove(1)  # удаляем 20
        self.assertEqual(len(self.array), 3)
        self.assertEqual(self.array[0], 10)
        self.assertEqual(self.array[1], 30)  # 30 сдвинулось влево
        self.assertEqual(self.array[2], 40)
        self.assertEqual(self.array.get_remove_status(), DynArray.REMOVE_OK)

        # Удаление первого элемента
        self.array.remove(0)  # удаляем 10
        self.assertEqual(len(self.array), 2)
        self.assertEqual(self.array[0], 30)
        self.assertEqual(self.array[1], 40)

        # Удаление последнего элемента
        self.array.remove(1)  # удаляем 40
        self.assertEqual(len(self.array), 1)
        self.assertEqual(self.array[0], 30)

    def test_remove_index_error(self):
        """Тест исключения при удалении по неверному индексу."""
        # Пустой массив
        with self.assertRaises(IndexError):
            self.array.remove(0)
        self.assertEqual(
            self.array.get_remove_status(), DynArray.REMOVE_ERR_INDEX
        )

        # Массив с элементами
        self.array.append(1)
        self.array.append(2)

        # Индекс больше длины
        with self.assertRaises(IndexError):
            self.array.remove(5)
        self.assertEqual(
            self.array.get_remove_status(), DynArray.REMOVE_ERR_INDEX
        )

        # Отрицательный индекс больше длины
        with self.assertRaises(IndexError):
            self.array.remove(-10)
        self.assertEqual(
            self.array.get_remove_status(), DynArray.REMOVE_ERR_INDEX
        )

    def test_insert_success(self):
        """Тест успешной вставки элемента."""
        # Вставка в пустой массив
        self.array.insert(0, 100)
        self.assertEqual(len(self.array), 1)
        self.assertEqual(self.array[0], 100)
        self.assertEqual(self.array.get_insert_status(), DynArray.INSERT_OK)

        # Вставка в начало
        self.array.insert(0, 50)
        self.assertEqual(len(self.array), 2)
        self.assertEqual(self.array[0], 50)
        self.assertEqual(self.array[1], 100)

        # Вставка в середину
        self.array.insert(1, 75)
        self.assertEqual(len(self.array), 3)
        self.assertEqual(self.array[0], 50)
        self.assertEqual(self.array[1], 75)
        self.assertEqual(self.array[2], 100)

        # Вставка в конец (аналогично append)
        self.array.insert(3, 200)
        self.assertEqual(len(self.array), 4)
        self.assertEqual(self.array[3], 200)

    def test_insert_index_error(self):
        """Тест исключения при вставке по неверному индексу."""
        # Вставка с индексом больше длины
        with self.assertRaises(IndexError):
            self.array.insert(5, 100)
        self.assertEqual(
            self.array.get_insert_status(), DynArray.INSERT_ERR_INDEX
        )

        # Отрицательный индекс больше длины
        with self.assertRaises(IndexError):
            self.array.insert(-10, 100)
        self.assertEqual(
            self.array.get_insert_status(), DynArray.INSERT_ERR_INDEX
        )

    def test_clear(self):
        """Тест очистки массива."""
        # Добавляем элементы
        self.array.append(1)
        self.array.append(2)
        self.array.append(3)
        self.assertEqual(len(self.array), 3)

        # Очищаем массив
        self.array.clear()
        self.assertEqual(len(self.array), 0)

        # Проверяем, что можно снова добавлять элементы
        self.array.append(10)
        self.assertEqual(len(self.array), 1)
        self.assertEqual(self.array[0], 10)

    def test_len(self):
        """Тест получения длины массива."""
        # Пустой массив
        self.assertEqual(len(self.array), 0)

        # Добавляем элементы
        self.array.append(1)
        self.assertEqual(len(self.array), 1)

        self.array.append(2)
        self.array.append(3)
        self.assertEqual(len(self.array), 3)

        # Удаляем элемент
        self.array.remove(0)
        self.assertEqual(len(self.array), 2)

        # Очищаем
        self.array.clear()
        self.assertEqual(len(self.array), 0)

    def test_get_min_capacity(self):
        """Тест получения минимальной емкости."""
        arr1 = DynArray[int](min_capacity=5)
        self.assertEqual(arr1.get_min_capacity(), 5)

        arr2 = DynArray[str](min_capacity=100)
        self.assertEqual(arr2.get_min_capacity(), 100)

    def test_edge_cases(self):
        """Тест граничных случаев."""
        # Создание массива с минимальной емкостью 1
        small_array = DynArray[int](min_capacity=1)
        self.assertEqual(small_array.get_min_capacity(), 1)

        # Добавление множества элементов (проверка динамического расширения)
        for i in range(100):
            small_array.append(i)

        self.assertEqual(len(small_array), 100)
        for i in range(100):
            self.assertEqual(small_array[i], i)

        # Удаление всех элементов по одному
        for i in range(100):
            small_array.remove(0)

        self.assertEqual(len(small_array), 0)

    def test_mixed_operations(self):
        """Тест комбинированных операций."""
        # Последовательность различных операций
        self.array.append(1)
        self.array.append(2)
        self.array.append(3)

        self.array.insert(1, 15)  # [1, 15, 2, 3]
        self.assertEqual(self.array[1], 15)

        self.array[2] = 25  # [1, 15, 25, 3]
        self.assertEqual(self.array[2], 25)

        self.array.remove(0)  # [15, 25, 3]
        self.assertEqual(len(self.array), 3)
        self.assertEqual(self.array[0], 15)

        self.array.append(100)  # [15, 25, 3, 100]
        self.assertEqual(len(self.array), 4)

        self.array.clear()
        self.assertEqual(len(self.array), 0)

    def test_capacity_expansion_on_append(self):
        """Тест расширения capacity при append."""
        # Создаем массив с малой начальной емкостью
        small_array = DynArray[int](min_capacity=4)
        self.assertEqual(small_array.capacity, 4)

        # Заполняем до полной емкости
        for i in range(4):
            small_array.append(i)
        self.assertEqual(len(small_array), 4)
        self.assertEqual(small_array.capacity, 4)

        # Добавляем еще один элемент - должно произойти расширение в 2 раза
        small_array.append(4)
        self.assertEqual(len(small_array), 5)
        self.assertEqual(small_array.capacity, 8)

        # Заполняем новую емкость
        for i in range(5, 8):
            small_array.append(i)
        self.assertEqual(len(small_array), 8)
        self.assertEqual(small_array.capacity, 8)

        # Еще одно расширение
        small_array.append(8)
        self.assertEqual(len(small_array), 9)
        self.assertEqual(small_array.capacity, 16)

    def test_capacity_expansion_on_insert(self):
        """Тест расширения capacity при insert."""
        small_array = DynArray[int](min_capacity=3)

        # Заполняем до полной емкости
        for i in range(3):
            small_array.append(i)
        self.assertEqual(small_array.capacity, 3)

        # Вставляем элемент - должно произойти расширение
        small_array.insert(1, 99)
        self.assertEqual(len(small_array), 4)
        self.assertEqual(small_array.capacity, 6)

        # Проверяем корректность данных после расширения
        self.assertEqual(small_array[0], 0)
        self.assertEqual(small_array[1], 99)
        self.assertEqual(small_array[2], 1)
        self.assertEqual(small_array[3], 2)

    def test_capacity_shrinking_on_remove(self):
        """Тест сжатия capacity при remove."""
        # Создаем массив и расширяем его
        arr = DynArray[int](min_capacity=4)

        # Заполняем до расширения
        for i in range(9):
            arr.append(i)
        self.assertEqual(
            arr.capacity, 16
        )  # Должно было расшириться: 4 -> 8 -> 16
        self.assertEqual(len(arr), 9)

        # Удаляем элементы до тех пор, пока length < 0.5 * capacity
        # При capacity=16, нужно чтобы length < 8
        while len(arr) >= 8:
            arr.remove(0)

        # Теперь length = 7, capacity должно сжаться
        # new_capacity = max(16 / 1.5, 4) = max(10.67, 4) = 10 (int)
        self.assertEqual(arr.capacity, 10)
        self.assertEqual(len(arr), 7)

    def test_capacity_min_limit_on_shrinking(self):
        """Тест ограничения минимальной емкости при сжатии."""
        arr = DynArray[int](min_capacity=8)

        # Заполняем массив
        for i in range(12):
            arr.append(i)
        self.assertEqual(arr.capacity, 16)  # 8 -> 16

        # Удаляем элементы до минимального размера
        while len(arr) > 1:
            arr.remove(0)

        # Capacity не должно стать меньше MIN_CAPACITY
        self.assertGreaterEqual(arr.capacity, 8)
        self.assertEqual(len(arr), 1)

    def test_capacity_reset_on_clear(self):
        """Тест сброса capacity при clear."""
        arr = DynArray[int](min_capacity=5)

        # Расширяем массив
        for i in range(15):
            arr.append(i)
        self.assertGreater(
            arr.capacity, 5
        )  # Должно быть больше минимальной емкости

        # Очищаем массив
        arr.clear()

        # Capacity должно вернуться к минимальному значению
        self.assertEqual(arr.capacity, 5)
        self.assertEqual(len(arr), 0)


if __name__ == "__main__":
    # Запуск всех тестов
    unittest.main(verbosity=2)
