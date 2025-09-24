import unittest
from typing import Any

from NativeDictionary import NativeDictionary


class TestNativeDictionary(unittest.TestCase):

    def setUp(self):
        self.dict = NativeDictionary(5)

    def test_constructor(self):
        self.assertEqual(self.dict.amount(), 0)
        self.assertEqual(self.dict.get_capacity(), 5)

    def test_put_basic(self):
        self.dict.put("key1", "value1")
        self.assertEqual(self.dict.get_put_status(), self.dict.PUT_OK)
        self.assertTrue(self.dict.contains("key1"))
        self.assertEqual(self.dict.amount(), 1)

        self.dict.put("key2", "value2")
        self.dict.put("key3", 123)
        self.assertEqual(self.dict.get_put_status(), self.dict.PUT_OK)
        self.assertEqual(self.dict.amount(), 3)

    def test_put_update_existing_key(self):
        self.dict.put("key1", "old_value")
        self.dict.put("key1", "new_value")

        self.assertEqual(self.dict.get_put_status(), self.dict.PUT_OK)
        self.assertEqual(self.dict.get("key1"), "new_value")
        self.assertEqual(self.dict.amount(), 1)

    def test_put_full_capacity(self):
        for i in range(5):
            self.dict.put(f"key{i}", f"value{i}")

        self.assertEqual(self.dict.amount(), 5)

        self.dict.put("overflow_key", "overflow_value")

        self.assertEqual(self.dict.get_put_status(), self.dict.PUT_ERR)

    def test_get_basic(self):
        self.dict.put("test_key", "test_value")
        self.dict.put("number_key", 42)

        value1 = self.dict.get("test_key")
        self.assertEqual(value1, "test_value")
        self.assertEqual(self.dict.get_get_status(), self.dict.GET_OK)

        value2 = self.dict.get("number_key")
        self.assertEqual(value2, 42)
        self.assertEqual(self.dict.get_get_status(), self.dict.GET_OK)

    def test_get_non_existing_key(self):
        with self.assertRaises(KeyError):
            result = self.dict.get("non_existing")
        self.assertEqual(self.dict.get_get_status(), self.dict.GET_NOT_FOUND)

        self.dict.put("existing", "value")
        with self.assertRaises(KeyError):
            result = self.dict.get("still_non_existing")
        self.assertEqual(self.dict.get_get_status(), self.dict.GET_NOT_FOUND)

    def test_contains(self):
        self.assertFalse(self.dict.contains("any_key"))

        self.dict.put("key1", "value1")
        self.dict.put("key2", 100)

        self.assertTrue(self.dict.contains("key1"))
        self.assertTrue(self.dict.contains("key2"))
        self.assertFalse(self.dict.contains("key3"))
        self.assertFalse(self.dict.contains(""))

    def test_remove_basic(self):
        self.dict.put("key1", "value1")
        self.dict.put("key2", "value2")
        self.assertEqual(self.dict.amount(), 2)

        self.dict.remove("key1")
        self.assertEqual(self.dict.get_remove_status(), self.dict.REMOVE_OK)
        self.assertFalse(self.dict.contains("key1"))
        self.assertEqual(self.dict.amount(), 1)

        self.assertTrue(self.dict.contains("key2"))

    def test_remove_non_existing_key(self):
        self.dict.remove("non_existing")
        self.assertEqual(
            self.dict.get_remove_status(),
            self.dict.REMOVE_NOT_FOUND,
        )

        self.dict.put("existing", "value")
        self.dict.remove("non_existing")
        self.assertEqual(
            self.dict.get_remove_status(),
            self.dict.REMOVE_NOT_FOUND,
        )

        self.assertTrue(self.dict.contains("existing"))
        self.assertEqual(self.dict.amount(), 1)

    def test_remove_all_elements(self):
        keys = ["key1", "key2", "key3"]
        for key in keys:
            self.dict.put(key, f"value_{key}")

        self.assertEqual(self.dict.amount(), 3)

        for key in keys:
            self.dict.remove(key)
            self.assertEqual(
                self.dict.get_remove_status(),
                self.dict.REMOVE_OK,
            )

        self.assertEqual(self.dict.amount(), 0)
        for key in keys:
            self.assertFalse(self.dict.contains(key))

    def test_capacity_and_amount(self):
        self.assertEqual(self.dict.get_capacity(), 5)
        self.assertEqual(self.dict.amount(), 0)

        for i in range(5):
            self.dict.put(f"key{i}", i)
            self.assertEqual(self.dict.amount(), i + 1)

        self.assertEqual(self.dict.get_capacity(), 5)

        for i in range(5):
            self.dict.remove(f"key{i}")
            self.assertEqual(self.dict.amount(), 5 - i - 1)

    def test_status_initialization(self):
        self.assertEqual(self.dict.get_put_status(), self.dict.PUT_NIL)
        self.assertEqual(self.dict.get_remove_status(), self.dict.REMOVE_NIL)
        self.assertEqual(self.dict.get_get_status(), self.dict.GET_NIL)

    def test_empty_string_key(self):
        self.dict.put("", "empty_key_value")
        self.assertEqual(self.dict.get_put_status(), self.dict.PUT_OK)

        self.assertTrue(self.dict.contains(""))
        self.assertEqual(self.dict.get(""), "empty_key_value")
        self.assertEqual(self.dict.get_get_status(), self.dict.GET_OK)

        self.dict.remove("")
        self.assertEqual(self.dict.get_remove_status(), self.dict.REMOVE_OK)
        self.assertFalse(self.dict.contains(""))


if __name__ == "__main__":
    unittest.main()
