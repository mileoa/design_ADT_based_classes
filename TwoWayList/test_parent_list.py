import unittest

from TwoWayList import LinkedList


class TestLinkedList(unittest.TestCase):
    """Тесты для класса LinkedList"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.list = LinkedList()

    def test_init(self):
        """Тест конструктора"""
        self.assertEqual(self.list.size(), 0)
        self.assertFalse(self.list.is_value())
        self.assertFalse(self.list.is_head())
        self.assertFalse(self.list.is_tail())

        self.assertEqual(self.list.get_head_status(), LinkedList.HEAD_NIL)
        self.assertEqual(self.list.get_tail_status(), LinkedList.TAIL_NIL)
        self.assertEqual(self.list.get_right_status(), LinkedList.RIGHT_NIL)
        self.assertEqual(
            self.list.get_put_right_status(), LinkedList.PUT_RIGHT_NIL
        )
        self.assertEqual(
            self.list.get_put_left_status(), LinkedList.PUT_LEFT_NIL
        )
        self.assertEqual(self.list.get_remove_status(), LinkedList.REMOVE_NIL)
        self.assertEqual(
            self.list.get_add_to_empty_status(), LinkedList.ADD_TO_EMPTY_NIL
        )
        self.assertEqual(self.list.get_replace_status(), LinkedList.REPLACE_NIL)
        self.assertEqual(self.list.get_find_status(), LinkedList.FIND_NIL)
        self.assertEqual(self.list.get_get_status(), LinkedList.GET_NIL)

    def test_add_to_empty_success(self):
        """Тест успешного добавления в пустой список"""
        self.list.add_to_empty(10)

        self.assertEqual(self.list.size(), 1)
        self.assertTrue(self.list.is_value())
        self.assertTrue(self.list.is_head())
        self.assertTrue(self.list.is_tail())
        self.assertEqual(self.list.get(), 10)
        self.assertEqual(
            self.list.get_add_to_empty_status(), LinkedList.ADD_TO_EMPTY_OK
        )

    def test_add_to_empty_error(self):
        """Тест ошибки при добавлении в непустой список"""
        self.list.add_to_empty(10)
        self.list.add_to_empty(20)  # Должна быть ошибка

        self.assertEqual(self.list.size(), 1)
        self.assertEqual(
            self.list.get_add_to_empty_status(), LinkedList.ADD_TO_EMPTY_ERR
        )

    def test_add_tail(self):
        """Тест добавления элементов в хвост"""
        # Добавление в пустой список
        self.list.add_tail(1)
        self.assertEqual(self.list.size(), 1)

        # Добавление в непустой список
        self.list.add_tail(2)
        self.list.add_tail(3)
        self.assertEqual(self.list.size(), 3)

        # Проверим, что элементы добавились правильно
        self.list.head()
        self.assertEqual(self.list.get(), 1)
        self.list.right()
        self.assertEqual(self.list.get(), 2)
        self.list.right()
        self.assertEqual(self.list.get(), 3)

    def test_head_success(self):
        """Тест успешного перехода к началу списка"""
        self.list.add_tail(1)
        self.list.add_tail(2)
        self.list.add_tail(3)

        self.list.tail()  # Переходим в хвост
        self.list.head()  # Возвращаемся в голову

        self.assertTrue(self.list.is_head())
        self.assertEqual(self.list.get(), 1)
        self.assertEqual(self.list.get_head_status(), LinkedList.HEAD_OK)

    def test_head_error(self):
        """Тест ошибки при переходе к началу пустого списка"""
        self.list.head()

        self.assertEqual(self.list.get_head_status(), LinkedList.HEAD_ERR_EMPTY)

    def test_tail_success(self):
        """Тест успешного перехода к концу списка"""
        self.list.add_tail(1)
        self.list.add_tail(2)
        self.list.add_tail(3)

        self.list.head()  # Переходим в голову
        self.list.tail()  # Переходим в хвост

        self.assertTrue(self.list.is_tail())
        self.assertEqual(self.list.get(), 3)
        self.assertEqual(self.list.get_tail_status(), LinkedList.TAIL_OK)

    def test_tail_error(self):
        """Тест ошибки при переходе к концу пустого списка"""
        self.list.tail()

        self.assertEqual(self.list.get_tail_status(), LinkedList.TAIL_ERR_EMPTY)

    def test_right_success(self):
        """Тест успешного движения вправо"""
        self.list.add_tail(1)
        self.list.add_tail(2)
        self.list.add_tail(3)

        self.list.head()
        self.assertEqual(self.list.get(), 1)

        self.list.right()
        self.assertEqual(self.list.get(), 2)
        self.assertEqual(self.list.get_right_status(), LinkedList.RIGHT_OK)

        self.list.right()
        self.assertEqual(self.list.get(), 3)
        self.assertEqual(self.list.get_right_status(), LinkedList.RIGHT_OK)

    def test_right_no_element(self):
        """Тест ошибки при движении вправо, когда нет элемента"""
        # Пустой список
        self.list.right()
        self.assertEqual(
            self.list.get_right_status(), LinkedList.RIGHT_NO_ELEMENT
        )

        # Последний элемент списка
        self.list.add_tail(1)
        self.list.head()
        self.list.right()  # Нет элемента справа
        self.assertEqual(
            self.list.get_right_status(), LinkedList.RIGHT_NO_ELEMENT
        )

    def test_put_right_success(self):
        """Тест успешной вставки справа"""
        self.list.add_tail(1)
        self.list.put_right(3)
        self.list.put_right(2)

        self.assertEqual(self.list.size(), 3)
        self.assertEqual(
            self.list.get_put_right_status(), LinkedList.PUT_RIGHT_OK
        )

        # Проверяем порядок элементов
        self.list.head()
        self.assertEqual(self.list.get(), 1)
        self.list.right()
        self.assertEqual(self.list.get(), 2)
        self.list.right()
        self.assertEqual(self.list.get(), 3)

    def test_put_right_error(self):
        """Тест ошибки при вставке справа в пустой список"""
        self.list.put_right(1)

        self.assertEqual(
            self.list.get_put_right_status(), LinkedList.PUT_RIGHT_ERR_EMPTY
        )
        self.assertEqual(self.list.size(), 0)

    def test_put_left_success(self):
        """Тест успешной вставки слева"""
        self.list.add_tail(3)

        self.list.put_left(1)
        self.list.put_left(2)

        self.assertEqual(self.list.size(), 3)
        self.assertEqual(
            self.list.get_put_left_status(), LinkedList.PUT_LEFT_OK
        )

        # Проверяем порядок элементов
        self.list.head()
        self.assertEqual(self.list.get(), 1)
        self.list.right()
        self.assertEqual(self.list.get(), 2)
        self.list.right()
        self.assertEqual(self.list.get(), 3)

    def test_put_left_error(self):
        """Тест ошибки при вставке слева в пустой список"""
        self.list.put_left(1)

        self.assertEqual(
            self.list.get_put_left_status(), LinkedList.PUT_LEFT_ERR_EMPTY
        )
        self.assertEqual(self.list.size(), 0)

    def test_remove_success(self):
        """Тест успешного удаления элемента"""
        self.list.add_tail(1)
        self.list.add_tail(2)
        self.list.add_tail(3)

        # Удаляем средний элемент
        self.list.head()
        self.list.right()  # Переходим на 2
        self.list.remove()

        self.assertEqual(self.list.size(), 2)
        self.assertEqual(self.list.get_remove_status(), LinkedList.REMOVE_OK)
        self.assertEqual(
            self.list.get(), 3
        )  # Курсор должен быть на правом соседе

        # Проверяем, что остались только 1 и 3
        self.list.head()
        self.assertEqual(self.list.get(), 1)
        self.list.right()
        self.assertEqual(self.list.get(), 3)

    def test_remove_single_element(self):
        """Тест удаления единственного элемента"""
        self.list.add_to_empty(42)
        self.list.remove()

        self.assertEqual(self.list.size(), 0)
        self.assertFalse(self.list.is_value())
        self.assertEqual(self.list.get_remove_status(), LinkedList.REMOVE_OK)

    def test_remove_error(self):
        """Тест ошибки при удалении из пустого списка"""
        self.list.remove()

        self.assertEqual(
            self.list.get_remove_status(), LinkedList.REMOVE_ERR_EMPTY
        )

    def test_clear(self):
        """Тест очистки списка"""
        self.list.add_tail(1)
        self.list.add_tail(2)
        self.list.add_tail(3)

        self.list.clear()

        self.assertEqual(self.list.size(), 0)
        self.assertFalse(self.list.is_value())

        # Проверяем, что все статусы сброшены
        self.assertEqual(self.list.get_head_status(), LinkedList.HEAD_NIL)
        self.assertEqual(self.list.get_tail_status(), LinkedList.TAIL_NIL)

    def test_replace_success(self):
        """Тест успешной замены значения"""
        self.list.add_to_empty(10)
        self.list.replace(20)

        self.assertEqual(self.list.get(), 20)
        self.assertEqual(self.list.get_replace_status(), LinkedList.REPLACE_OK)

    def test_replace_error(self):
        """Тест ошибки при замене в пустом списке"""
        self.list.replace(10)

        self.assertEqual(
            self.list.get_replace_status(), LinkedList.REPLACE_ERR_EMPTY
        )

    def test_find_success(self):
        """Тест успешного поиска"""
        self.list.add_tail(1)
        self.list.add_tail(2)
        self.list.add_tail(3)
        self.list.add_tail(2)

        self.list.head()
        self.list.find(2)

        self.assertEqual(self.list.get(), 2)
        self.assertEqual(self.list.get_find_status(), LinkedList.FIND_OK)

    def test_find_not_found(self):
        """Тест поиска несуществующего элемента"""
        self.list.add_tail(1)
        self.list.add_tail(2)
        self.list.add_tail(3)

        self.list.head()
        initial_position = self.list.get()
        self.list.find(5)  # Элемента нет

        self.assertEqual(
            self.list.get(), initial_position
        )  # Курсор не должен сдвинуться
        self.assertEqual(
            self.list.get_find_status(), LinkedList.FIND_ERR_NOT_FOUND
        )

    def test_find_error_empty(self):
        """Тест ошибки поиска в пустом списке"""
        self.list.find(1)

        self.assertEqual(self.list.get_find_status(), LinkedList.FIND_ERR_EMPTY)

    def test_remove_all(self):
        """Тест удаления всех элементов с заданным значением"""
        self.list.add_tail(1)
        self.list.add_tail(2)
        self.list.add_tail(1)
        self.list.add_tail(3)
        self.list.add_tail(1)

        self.list.head()
        self.list.remove_all(1)

        self.assertEqual(self.list.size(), 2)

        # Проверяем, что остались только 2 и 3
        self.list.head()
        self.assertEqual(self.list.get(), 2)
        self.list.right()
        self.assertEqual(self.list.get(), 3)

    def test_remove_all_empty_list(self):
        """Тест удаления всех элементов из пустого списка"""
        self.list.remove_all(1)
        self.assertEqual(self.list.size(), 0)

    def test_get_success(self):
        """Тест успешного получения значения"""
        self.list.add_to_empty(42)
        value = self.list.get()

        self.assertEqual(value, 42)
        self.assertEqual(self.list.get_get_status(), LinkedList.GET_OK)

    def test_get_error(self):
        """Тест ошибки при получении значения из пустого списка"""
        with self.assertRaises(ValueError):
            self.list.get()

        self.assertEqual(self.list.get_get_status(), LinkedList.GET_ERR_EMPTY)

    def test_is_head(self):
        """Тест проверки, находится ли курсор в начале"""
        self.list.add_tail(1)
        self.list.add_tail(2)

        self.list.head()
        self.assertTrue(self.list.is_head())

        self.list.right()
        self.assertFalse(self.list.is_head())

    def test_is_tail(self):
        """Тест проверки, находится ли курсор в конце"""
        self.list.add_tail(1)
        self.list.add_tail(2)

        self.list.tail()
        self.assertTrue(self.list.is_tail())

        self.list.head()
        self.assertFalse(self.list.is_tail())

    def test_is_value(self):
        """Тест проверки, установлен ли курсор"""
        self.assertFalse(self.list.is_value())

        self.list.add_to_empty(1)
        self.assertTrue(self.list.is_value())

        self.list.remove()
        self.assertFalse(self.list.is_value())

    def test_complex_scenario(self):
        """Комплексный тест различных операций"""
        # Создаем список [1, 2, 3, 4, 5]
        for i in range(1, 6):
            self.list.add_tail(i)

        # Переходим к элементу 3
        self.list.head()
        self.list.right()
        self.list.right()
        self.assertEqual(self.list.get(), 3)

        # Вставляем 2.5 слева от 3
        self.list.put_left(2.5)
        self.assertEqual(self.list.size(), 6)

        # Вставляем 3.5 справа от 3
        self.list.put_right(3.5)
        self.assertEqual(self.list.size(), 7)

        # Проверяем последовательность
        expected = [1, 2, 2.5, 3, 3.5, 4, 5]
        self.list.head()
        for expected_value in expected:
            self.assertEqual(self.list.get(), expected_value)
            if not self.list.is_tail():
                self.list.right()

        # Удаляем все элементы со значением больше 4
        self.list.remove_all(5)
        self.assertEqual(self.list.size(), 6)

        # Заменяем текущее значение
        self.list.head()
        self.list.replace(0)
        self.assertEqual(self.list.get(), 0)


if __name__ == "__main__":
    unittest.main()
