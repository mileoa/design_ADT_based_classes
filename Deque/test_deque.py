import unittest
from Deque import Deque


class TestDeque(unittest.TestCase):

    def setUp(self):
        self.deque = Deque()

    def test_regression_add_tail(self):
        self.assertEqual(self.deque.size(), 0)
        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_NIL)
        self.assertEqual(self.deque.get_get_tail_status(), Deque.GET_TAIL_NIL)
        self.assertEqual(self.deque.get_remove_head_status(), Deque.REMOVE_HEAD_NIL)
        self.assertEqual(self.deque.get_remove_tail_status(), Deque.REMOVE_TAIL_NIL)

        for i in range(5):
            self.deque.add_tail(i)
            self.assertEqual(self.deque.get_head(), 0)
            self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_OK)
            self.assertEqual(self.deque.size(), i + 1)

        for i in range(7):
            if i < 5:
                self.deque.remove_head()
                self.assertEqual(self.deque.size(), 4 - i)
                self.assertEqual(
                    self.deque.get_remove_head_status(), Deque.REMOVE_HEAD_OK
                )
                continue
            with self.assertRaises(IndexError):
                self.deque.remove_head()
            with self.assertRaises(IndexError):
                self.deque.get_head()
            self.assertEqual(self.deque.size(), 0)
            self.assertEqual(
                self.deque.get_remove_head_status(), Deque.REMOVE_HEAD_EMPTY
            )
            self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_EMPTY)

        self.deque.add_tail(7)
        self.assertEqual(self.deque.size(), 1)
        self.assertEqual(self.deque.get_head(), 7)
        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_OK)

    def test_empty_deque_initial_state(self):
        self.assertEqual(self.deque.size(), 0)

        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_NIL)
        self.assertEqual(self.deque.get_get_tail_status(), Deque.GET_TAIL_NIL)
        self.assertEqual(self.deque.get_remove_head_status(), Deque.REMOVE_HEAD_NIL)
        self.assertEqual(self.deque.get_remove_tail_status(), Deque.REMOVE_TAIL_NIL)

    def test_add_tail(self):
        self.deque.add_tail(1)
        self.assertEqual(self.deque.size(), 1)
        self.assertEqual(self.deque.get_head(), 1)
        self.assertEqual(self.deque.get_tail(), 1)

        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_OK)
        self.assertEqual(self.deque.get_get_tail_status(), Deque.GET_TAIL_OK)

        self.deque.add_tail(2)
        self.assertEqual(self.deque.size(), 2)
        self.assertEqual(self.deque.get_head(), 1)
        self.assertEqual(self.deque.get_tail(), 2)

        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_OK)
        self.assertEqual(self.deque.get_get_tail_status(), Deque.GET_TAIL_OK)

    def test_add_head(self):
        self.deque.add_head(1)
        self.assertEqual(self.deque.size(), 1)
        self.assertEqual(self.deque.get_head(), 1)
        self.assertEqual(self.deque.get_tail(), 1)
        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_OK)
        self.assertEqual(self.deque.get_get_tail_status(), Deque.GET_TAIL_OK)

        self.deque.add_head(2)
        self.assertEqual(self.deque.size(), 2)
        self.assertEqual(self.deque.get_head(), 2)
        self.assertEqual(self.deque.get_tail(), 1)
        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_OK)
        self.assertEqual(self.deque.get_get_tail_status(), Deque.GET_TAIL_OK)

    def test_remove_head(self):
        self.deque.add_tail(1)
        self.deque.add_tail(2)

        self.deque.remove_head()
        self.assertEqual(self.deque.size(), 1)
        self.assertEqual(self.deque.get_head(), 2)
        self.assertEqual(self.deque.get_remove_head_status(), Deque.REMOVE_HEAD_OK)
        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_OK)

    def test_remove_tail(self):
        self.deque.add_tail(1)
        self.deque.add_tail(2)

        self.deque.remove_tail()
        self.assertEqual(self.deque.size(), 1)
        self.assertEqual(self.deque.get_head(), 1)
        self.assertEqual(self.deque.get_remove_tail_status(), Deque.REMOVE_TAIL_OK)
        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_TAIL_OK)

    def test_get_head_empty_deque(self):
        with self.assertRaises(IndexError):
            self.deque.get_head()
        self.assertEqual(self.deque.get_get_head_status(), Deque.GET_HEAD_EMPTY)

    def test_get_tail_empty_deque(self):
        with self.assertRaises(IndexError):
            self.deque.get_tail()
        self.assertEqual(self.deque.get_get_tail_status(), Deque.GET_TAIL_EMPTY)

    def test_remove_head_empty_deque(self):
        with self.assertRaises(IndexError):
            self.deque.remove_head()
        self.assertEqual(self.deque.get_remove_head_status(), Deque.REMOVE_HEAD_EMPTY)

    def test_remove_tail_empty_deque(self):
        with self.assertRaises(IndexError):
            self.deque.remove_tail()
        self.assertEqual(self.deque.get_remove_tail_status(), Deque.REMOVE_TAIL_EMPTY)

    def test_multiple_add_and_remove(self):
        for i in range(5):
            self.deque.add_tail(i)

        self.assertEqual(self.deque.size(), 5)
        self.assertEqual(self.deque.get_head(), 0)
        self.assertEqual(self.deque.get_tail(), 4)

        self.deque.remove_head()
        self.assertEqual(self.deque.size(), 4)
        self.assertEqual(self.deque.get_head(), 1)

        self.deque.remove_tail()
        self.assertEqual(self.deque.size(), 3)
        self.assertEqual(self.deque.get_tail(), 3)

    def test_edge_cases(self):
        self.deque.add_tail(1)
        self.deque.remove_head()
        self.assertEqual(self.deque.size(), 0)

        self.deque.add_head(2)
        self.deque.remove_tail()
        self.assertEqual(self.deque.size(), 0)

    def tearDown(self):
        self.deque = None


if __name__ == "__main__":
    unittest.main()
