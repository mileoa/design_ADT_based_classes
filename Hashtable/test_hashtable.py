import unittest

from Hashtable import Hashtable


class TestHashtable(unittest.TestCase):

    def setUp(self) -> None:
        self.capacity: int = 10
        self.table: Hashtable[int] = Hashtable[int](self.capacity)

    def test_init_zero_capacity(self):
        with self.assertRaises(ValueError):
            table: Hashtable[int] = Hashtable[int](0)

    def test_init_negative_capacity(self):
        with self.assertRaises(ValueError):
            table: Hashtable[int] = Hashtable[int](-1)

    def test_init(self):
        table = Hashtable(10)
        self.assertEqual(table.get_capacity(), 10)
        self.assertEqual(table.amount(), 0)
        self.assertEqual(table.get_put_status(), Hashtable.PUT_NIL)
        self.assertEqual(table.get_remove_status(), Hashtable.REMOVE_NIL)

    def test_put_not_full_table(self):
        for i in range(10):
            self.table.put(i)
            self.assertEqual(self.table.get_put_status(), Hashtable.PUT_OK)
            self.assertEqual(self.table.amount(), i + 1)

    def test_put_full_table(self):
        for i in range(10):
            self.table.put(i)

        elements_amount_before_put: int = self.table.amount()

        self.table.put(11)

        self.assertEqual(self.table.get_put_status(), Hashtable.PUT_ERR)
        self.assertEqual(self.table.amount(), elements_amount_before_put)

    def test_remove(self):
        self.table.put(600)

        self.table.remove(600)
        self.assertEqual(self.table.get_remove_status(), Hashtable.REMOVE_OK)
        self.assertEqual(self.table.amount(), 0)

    def test_remove_not_existing_element(self):
        for i in range(self.capacity):
            self.table.put(i)

        for i in range(self.capacity, self.capacity * 9):
            self.table.remove(i)
            self.assertEqual(
                self.table.get_remove_status(), Hashtable.REMOVE_NOT_FOUND
            )
            self.assertEqual(self.table.amount(), self.capacity)

    def test_remove_empty_table(self):
        self.table.remove(1)
        self.assertEqual(
            self.table.get_remove_status(), Hashtable.REMOVE_NOT_FOUND
        )
        self.assertEqual(self.table.amount(), 0)

    def test_contains_empty_table(self):
        self.assertFalse(self.table.contains(1))

    def test_contains_exists(self):
        for i in range(self.capacity):
            self.table.put(i)

        for i in range(self.capacity):
            self.assertTrue(self.table.contains(i))

    def test_contains_not_exists(self):
        for i in range(self.capacity):
            self.table.put(i)

        for i in range(self.capacity, self.capacity * 9):
            self.assertFalse(self.table.contains(i))

    def tearDown(self):
        self.assertEqual(self.table.get_capacity(), self.capacity)


if __name__ == "__main__":
    unittest.main()
