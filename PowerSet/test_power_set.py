import unittest
from typing import Any

from PowerSet import PowerSet


class TestPowerSet(unittest.TestCase):

    def setUp(self):
        self.power_set = PowerSet(10)

    # Тесты конструктора
    def test_constructor_creates_empty_set(self):
        ps = PowerSet(5)
        self.assertEqual(ps.amount(), 0)
        self.assertEqual(ps.get_capacity(), 5)

    # Тесты команды put()
    def test_put_new_element(self):
        """put() добавляет новый элемент"""
        self.power_set.put("элемент1")
        self.assertEqual(self.power_set.get_put_status(), PowerSet.PUT_OK)
        self.assertTrue(self.power_set.contains("элемент1"))
        self.assertEqual(self.power_set.amount(), 1)

    def test_put_existing_element(self):
        """put() не добавляет существующий элемент"""
        self.power_set.put("элемент1")
        self.power_set.put("элемент1")
        self.assertEqual(self.power_set.get_put_status(), PowerSet.PUT_OK)
        self.assertEqual(self.power_set.amount(), 1)

    def test_put_full_table_collision_error(self):
        """put() возвращает ошибку при невозможности разрешить коллизию"""
        ps = PowerSet(2)
        # Добавляем элементы до заполнения и возникновения коллизий
        ps.put("a")
        ps.put("b")
        ps.put("c")  # должна возникнуть ошибка
        self.assertEqual(ps.get_put_status(), PowerSet.PUT_ERR)

    def test_put_status_nil_initially(self):
        """Статус put() изначально равен PUT_NIL"""
        ps = PowerSet(5)
        self.assertEqual(ps.get_put_status(), PowerSet.PUT_NIL)

    # Тесты команды remove()
    def test_remove_existing_element(self):
        """remove() удаляет существующий элемент"""
        self.power_set.put("элемент1")
        self.power_set.remove("элемент1")
        self.assertEqual(
            self.power_set.get_remove_status(), PowerSet.REMOVE_OK
        )
        self.assertFalse(self.power_set.contains("элемент1"))
        self.assertEqual(self.power_set.amount(), 0)

    def test_remove_nonexisting_element(self):
        """remove() возвращает ошибку для несуществующего элемента"""
        self.power_set.remove("несуществующий")
        self.assertEqual(
            self.power_set.get_remove_status(), PowerSet.REMOVE_NOT_FOUND
        )

    def test_remove_status_nil_initially(self):
        """Статус remove() изначально равен REMOVE_NIL"""
        ps = PowerSet(5)
        self.assertEqual(ps.get_remove_status(), PowerSet.REMOVE_NIL)

    # Тесты запроса contains()
    def test_contains_existing_element(self):
        """contains() возвращает True для существующего элемента"""
        self.power_set.put("элемент1")
        self.assertTrue(self.power_set.contains("элемент1"))

    def test_contains_nonexisting_element(self):
        """contains() возвращает False для несуществующего элемента"""
        self.assertFalse(self.power_set.contains("несуществующий"))

    # Тесты команды intersect()
    def test_intersect_with_common_elements(self):
        """intersect() оставляет только общие элементы"""
        self.power_set.put("a")
        self.power_set.put("b")
        self.power_set.put("c")

        other_set = PowerSet(10)
        other_set.put("b")
        other_set.put("c")
        other_set.put("d")

        self.power_set.intersect(other_set)

        self.assertEqual(self.power_set.amount(), 2)
        self.assertFalse(self.power_set.contains("a"))
        self.assertTrue(self.power_set.contains("b"))
        self.assertTrue(self.power_set.contains("c"))
        self.assertFalse(self.power_set.contains("d"))

    def test_intersect_with_no_common_elements(self):
        """intersect() создает пустое множество при отсутствии общих элементов"""
        self.power_set.put("a")
        self.power_set.put("b")

        other_set = PowerSet(10)
        other_set.put("c")
        other_set.put("d")

        self.power_set.intersect(other_set)

        self.assertEqual(self.power_set.amount(), 0)
        self.assertFalse(self.power_set.contains("a"))
        self.assertFalse(self.power_set.contains("b"))
        self.assertFalse(self.power_set.contains("c"))
        self.assertFalse(self.power_set.contains("d"))

    def test_intersect_with_empty_set(self):
        """intersect() с пустым множеством создает пустое множество"""
        self.power_set.put("a")
        self.power_set.put("b")

        other_set = PowerSet(10)
        self.power_set.intersect(other_set)

        self.assertEqual(self.power_set.amount(), 0)
        self.assertFalse(self.power_set.contains("a"))
        self.assertFalse(self.power_set.contains("b"))

    # Тесты команды union()
    def test_union_adds_new_elements(self):
        """union() добавляет новые элементы из другого множества"""
        self.power_set.put("a")
        self.power_set.put("b")

        other_set = PowerSet(10)
        other_set.put("c")
        other_set.put("d")

        self.power_set.union(other_set)

        self.assertEqual(self.power_set.get_union_status(), PowerSet.UNION_OK)
        self.assertEqual(self.power_set.amount(), 4)
        self.assertTrue(self.power_set.contains("a"))
        self.assertTrue(self.power_set.contains("b"))
        self.assertTrue(self.power_set.contains("c"))
        self.assertTrue(self.power_set.contains("d"))

    def test_union_does_not_add_duplicates(self):
        """union() не добавляет дубликаты"""
        self.power_set.put("a")
        self.power_set.put("b")

        other_set = PowerSet(10)
        other_set.put("b")
        other_set.put("c")

        self.power_set.union(other_set)

        self.assertEqual(self.power_set.get_union_status(), PowerSet.UNION_OK)
        self.assertEqual(self.power_set.amount(), 3)

    def test_union_fails_when_capacity_exceeded(self):
        """union() возвращает ошибку при превышении вместимости"""
        ps = PowerSet(3)
        ps.put("a")
        ps.put("b")

        other_set = PowerSet(10)
        other_set.put("c")
        other_set.put("d")
        other_set.put("e")

        ps.union(other_set)

        self.assertEqual(ps.get_union_status(), PowerSet.UNION_ERR_FULL)

    def test_union_status_nil_initially(self):
        """Статус union() изначально равен UNION_NIL"""
        ps = PowerSet(5)
        self.assertEqual(ps.get_union_status(), PowerSet.UNION_NIL)

    # Тесты команды differ()
    def test_differ_removes_common_and_adds_different(self):
        """differ() удаляет общие и добавляет различающиеся элементы"""
        self.power_set.put("a")
        self.power_set.put("b")
        self.power_set.put("c")

        other_set = PowerSet(10)
        other_set.put("b")
        other_set.put("d")
        other_set.put("e")

        self.power_set.differ(other_set)

        self.assertEqual(
            self.power_set.get_differ_status(), PowerSet.DIFFER_OK
        )
        self.assertTrue(self.power_set.contains("a"))
        self.assertFalse(self.power_set.contains("b"))
        self.assertTrue(self.power_set.contains("c"))
        self.assertTrue(self.power_set.contains("d"))
        self.assertTrue(self.power_set.contains("e"))

    def test_differ_fails_when_capacity_exceeded(self):
        """differ() возвращает ошибку при превышении вместимости"""
        ps = PowerSet(3)
        ps.put("a")

        other_set = PowerSet(10)
        other_set.put("b")
        other_set.put("c")
        other_set.put("d")
        other_set.put("e")

        ps.differ(other_set)

        self.assertEqual(ps.get_differ_status(), PowerSet.DIFFER_ERR_FULL)

    def test_differ_status_nil_initially(self):
        """Статус differ() изначально равен DIFFER_NIL"""
        ps = PowerSet(5)
        self.assertEqual(ps.get_differ_status(), PowerSet.DIFFER_NIL)

    # Тесты запроса count_same()
    def test_count_same_with_common_elements(self):
        """count_same() возвращает количество общих элементов"""
        self.power_set.put("a")
        self.power_set.put("b")
        self.power_set.put("c")

        other_set = PowerSet(10)
        other_set.put("b")
        other_set.put("c")
        other_set.put("d")

        self.assertEqual(self.power_set.count_same(other_set), 2)

    def test_count_same_with_no_common_elements(self):
        """count_same() возвращает 0 при отсутствии общих элементов"""
        self.power_set.put("a")
        self.power_set.put("b")

        other_set = PowerSet(10)
        other_set.put("c")
        other_set.put("d")

        self.assertEqual(self.power_set.count_same(other_set), 0)

    def test_count_same_with_empty_sets(self):
        """count_same() возвращает 0 для пустых множеств"""
        other_set = PowerSet(10)
        self.assertEqual(self.power_set.count_same(other_set), 0)

    # Тесты запроса count_different()
    def test_count_different_with_different_elements(self):
        """count_different() возвращает количество различающихся элементов"""
        self.power_set.put("a")
        self.power_set.put("b")
        self.power_set.put("c")

        other_set = PowerSet(10)
        other_set.put("b")
        other_set.put("d")
        other_set.put("e")

        # Различающиеся: a, c (из текущего), d, e (из другого) = 4
        self.assertEqual(self.power_set.count_different(other_set), 4)

    def test_count_different_with_identical_sets(self):
        """count_different() возвращает 0 для идентичных множеств"""
        self.power_set.put("a")
        self.power_set.put("b")

        other_set = PowerSet(10)
        other_set.put("a")
        other_set.put("b")

        self.assertEqual(self.power_set.count_different(other_set), 0)

    def test_count_different_with_completely_different_sets(self):
        """count_different() возвращает сумму размеров для полностью различных множеств"""
        self.power_set.put("a")
        self.power_set.put("b")

        other_set = PowerSet(10)
        other_set.put("c")
        other_set.put("d")
        other_set.put("e")

        self.assertEqual(self.power_set.count_different(other_set), 5)

    # Тесты запросов get_capacity() и amount()
    def test_get_capacity_returns_correct_value(self):
        """get_capacity() возвращает корректную вместимость"""
        ps = PowerSet(15)
        self.assertEqual(ps.get_capacity(), 15)

    def test_amount_returns_correct_count(self):
        """amount() возвращает корректное количество элементов"""
        self.power_set.put("a")
        self.power_set.put("b")
        self.power_set.put("c")
        self.assertEqual(self.power_set.amount(), 3)

    def test_amount_after_remove(self):
        """amount() корректно уменьшается после удаления"""
        self.power_set.put("a")
        self.power_set.put("b")
        self.power_set.remove("a")
        self.assertEqual(self.power_set.amount(), 1)


if __name__ == "__main__":
    unittest.main()
