import unittest
from typing import Any

from BoundedStack import BoundedStack


class TestBoundedStack(unittest.TestCase):

    def setUp(self):
        self.stack = BoundedStack[int](max_size=3)
        self.large_stack = BoundedStack[str](max_size=100)

    def test_initialization_valid_size(self):
        stack = BoundedStack[int](5)
        self.assertEqual(stack.size(), 0)
        self.assertEqual(stack.get_push_status(), BoundedStack.PUSH_NIL)
        self.assertEqual(stack.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(stack.get_peek_status(), BoundedStack.PEEK_NIL)

    def test_initialization_default_size(self):
        stack = BoundedStack[int]()
        self.assertEqual(stack.size(), 0)
        for i in range(32):
            stack.push(i)
        self.assertEqual(stack.size(), 32)

    def test_initialization_invalid_size(self):
        with self.assertRaises(ValueError) as context:
            BoundedStack[int](0)
        self.assertIn("max_size должен быть > 0", str(context.exception))

        with self.assertRaises(ValueError) as context:
            BoundedStack[int](-5)
        self.assertIn("max_size должен быть > 0", str(context.exception))

    def test_push_single_element(self):
        self.stack.push(42)
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.get_push_status(), BoundedStack.PUSH_OK)

    def test_push_multiple_elements(self):
        elements = [1, 2, 3]
        for elem in elements:
            self.stack.push(elem)
            self.assertEqual(self.stack.get_push_status(), BoundedStack.PUSH_OK)
        self.assertEqual(self.stack.size(), 3)

    def test_push_to_full_stack(self):
        for i in range(3):
            self.stack.push(i)
        self.stack.push(999)
        self.assertEqual(self.stack.size(), 3)
        self.assertEqual(self.stack.get_push_status(), BoundedStack.PUSH_ERR)

    def test_pop_single_element(self):
        self.stack.push(42)
        initial_size = self.stack.size()
        self.stack.pop()
        self.assertEqual(self.stack.size(), initial_size - 1)
        self.assertEqual(self.stack.get_pop_status(), BoundedStack.POP_OK)

    def test_pop_multiple_elements(self):
        for i in range(3):
            self.stack.push(i)

        for _ in range(3):
            self.stack.pop()
            self.assertEqual(self.stack.get_pop_status(), BoundedStack.POP_OK)
        self.assertEqual(self.stack.size(), 0)

    def test_pop_from_empty_stack(self):
        self.assertEqual(self.stack.size(), 0)
        self.stack.pop()
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(self.stack.get_pop_status(), BoundedStack.POP_ERR)

    def test_peek_existing_element(self):
        self.stack.push(42)
        result = self.stack.peek()
        self.assertEqual(result, 42)
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.get_peek_status(), BoundedStack.PEEK_OK)

    def test_peek_last_added_element(self):
        elements = [1, 2, 3]
        for elem in elements:
            self.stack.push(elem)

        result = self.stack.peek()
        self.assertEqual(result, 3)  # последний добавленный элемент
        self.assertEqual(self.stack.get_peek_status(), BoundedStack.PEEK_OK)

    def test_peek_empty_stack(self):
        result = self.stack.peek()
        self.assertEqual(result, 0)
        self.assertEqual(self.stack.get_peek_status(), BoundedStack.PEEK_ERR)

    def test_clear_empty_stack(self):
        self.stack.clear()
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(self.stack.get_push_status(), BoundedStack.PUSH_NIL)
        self.assertEqual(self.stack.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(self.stack.get_peek_status(), BoundedStack.PEEK_NIL)

    def test_clear_filled_stack(self):
        """Тест очистки заполненного стека"""
        for i in range(3):
            self.stack.push(i)

        # Выполняем операцию для установки статуса
        self.stack.peek()

        self.stack.clear()
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(self.stack.get_push_status(), BoundedStack.PUSH_NIL)
        self.assertEqual(self.stack.get_pop_status(), BoundedStack.POP_NIL)
        self.assertEqual(self.stack.get_peek_status(), BoundedStack.PEEK_NIL)

    def test_lifo_behavior(self):
        elements = [1, 2, 3]

        # Добавляем элементы
        for elem in elements:
            self.stack.push(elem)

        # Проверяем, что элементы извлекаются в обратном порядке
        expected_order = [3, 2, 1]
        for expected in expected_order:
            actual = self.stack.peek()
            self.assertEqual(actual, expected)
            self.stack.pop()

    def test_generic_type_string(self):
        """Тест работы с строковыми типами"""
        string_stack = BoundedStack[str](5)
        test_strings = ["hello", "world", "test"]

        for s in test_strings:
            string_stack.push(s)

        self.assertEqual(string_stack.size(), 3)
        self.assertEqual(string_stack.peek(), "test")

        string_stack.pop()
        self.assertEqual(string_stack.peek(), "world")

    def test_edge_case_single_element_stack(self):
        tiny_stack = BoundedStack[int](1)

        # Добавляем элемент
        tiny_stack.push(42)
        self.assertEqual(tiny_stack.size(), 1)

        # Пытаемся добавить еще один
        tiny_stack.push(99)
        self.assertEqual(tiny_stack.size(), 1)
        self.assertEqual(tiny_stack.get_push_status(), BoundedStack.PUSH_ERR)

        self.assertEqual(tiny_stack.peek(), 42)

    def test_complex_scenario(self):
        self.stack.push(1)
        self.stack.push(2)

        self.stack.pop()
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), 1)

        self.stack.push(3)
        self.stack.push(4)
        self.assertEqual(self.stack.size(), 3)

        self.stack.push(5)
        self.assertEqual(self.stack.size(), 3)
        self.assertEqual(self.stack.get_push_status(), BoundedStack.PUSH_ERR)

        self.assertEqual(self.stack.peek(), 4)

    def test_status_persistence(self):
        """Тест сохранения статусов между операциями"""
        # Тестируем статус ошибки pop
        self.stack.pop()  # pop из пустого стека
        self.assertEqual(self.stack.get_pop_status(), BoundedStack.POP_ERR)

        # Статус должен сохраняться до следующей операции pop
        self.stack.push(1)
        self.assertEqual(self.stack.get_pop_status(), BoundedStack.POP_ERR)

        self.stack.pop()
        self.assertEqual(self.stack.get_pop_status(), BoundedStack.POP_OK)


if __name__ == "__main__":
    unittest.main()
