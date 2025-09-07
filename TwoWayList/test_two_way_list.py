import unittest

from TwoWayList import TwoWayList


class TestTwoWayListLeftMethod(unittest.TestCase):
    """Тесты для метода left() класса TwoWayList"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.lst = TwoWayList[int]()

    def test_initial_left_status(self):
        """Тест начального статуса left после создания списка"""
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_NIL)

    def test_left_on_empty_list(self):
        """Тест left() на пустом списке"""
        self.lst.left()

        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_NO_ELEMENT)
        self.assertIsNone(self.lst._cursor)
        self.assertEqual(self.lst.size(), 0)

    def test_left_at_head_single_element(self):
        """Тест left() когда курсор на единственном элементе"""
        self.lst.add_to_empty(10)
        self.lst.head()

        # Проверяем что курсор установлен на единственный элемент
        self.assertTrue(self.lst.is_head())
        self.assertTrue(self.lst.is_tail())

        self.lst.left()

        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_NO_ELEMENT)
        # Курсор должен остаться на том же элементе
        self.assertEqual(self.lst.get(), 10)

    def test_left_success_from_second_element(self):
        """Тест успешного left() с второго элемента на первый"""
        self.lst.add_to_empty(10)
        self.lst.add_tail(20)
        self.lst.add_tail(30)

        # Устанавливаем курсор на второй элемент
        self.lst.head()
        self.lst.right()
        self.assertEqual(self.lst.get(), 20)

        self.lst.left()

        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_OK)
        self.assertEqual(self.lst.get(), 10)
        self.assertTrue(self.lst.is_head())

    def test_left_success_multiple_moves(self):
        """Тест нескольких успешных перемещений left()"""
        self.lst.add_to_empty(10)
        self.lst.add_tail(20)
        self.lst.add_tail(30)
        self.lst.add_tail(40)

        # Начинаем с хвоста и идем влево
        self.lst.tail()
        self.assertEqual(self.lst.get(), 40)

        # Первое перемещение влево
        self.lst.left()
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_OK)
        self.assertEqual(self.lst.get(), 30)

        # Второе перемещение влево
        self.lst.left()
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_OK)
        self.assertEqual(self.lst.get(), 20)

        # Третье перемещение влево (должны достичь головы)
        self.lst.left()
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_OK)
        self.assertEqual(self.lst.get(), 10)
        self.assertTrue(self.lst.is_head())

        # Четвертое перемещение влево (должно быть невозможно)
        self.lst.left()
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_NO_ELEMENT)
        self.assertEqual(self.lst.get(), 10)  # Курсор остался на том же месте

    def test_left_after_right_sequence(self):
        """Тест left() после последовательности right()"""
        self.lst.add_to_empty(10)
        self.lst.add_tail(20)
        self.lst.add_tail(30)
        self.lst.add_tail(40)

        # Начинаем с головы и идем вправо
        self.lst.head()
        self.lst.right()  # на 20
        self.lst.right()  # на 30
        self.assertEqual(self.lst.get(), 30)

        # Теперь идем влево
        self.lst.left()  # на 20
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_OK)
        self.assertEqual(self.lst.get(), 20)

        self.lst.left()  # на 10
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_OK)
        self.assertEqual(self.lst.get(), 10)
        self.assertTrue(self.lst.is_head())

    def test_left_after_modifications(self):
        """Тест left() после модификаций списка"""
        self.lst.add_to_empty(10)
        self.lst.add_tail(20)
        self.lst.add_tail(30)

        # Устанавливаем курсор на средний элемент
        self.lst.head()
        self.lst.right()
        self.assertEqual(self.lst.get(), 20)

        # Добавляем элемент слева
        self.lst.put_left(15)
        self.assertEqual(self.lst.size(), 4)
        self.assertEqual(self.lst.get(), 20)  # Курсор остался на 20

        # Теперь идем влево - должны попасть на добавленный элемент
        self.lst.left()
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_OK)
        self.assertEqual(self.lst.get(), 15)

        # Еще раз влево - должны попасть на первый элемент
        self.lst.left()
        self.assertEqual(self.lst.get_left_status(), TwoWayList.LEFT_OK)
        self.assertEqual(self.lst.get(), 10)
        self.assertTrue(self.lst.is_head())


if __name__ == "__main__":
    unittest.main()
