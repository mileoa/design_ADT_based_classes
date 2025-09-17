import unittest
from Deque import ParentQueue


class QueueTests(unittest.TestCase):

    def setUp(self):
        self.q = ParentQueue()

    def test_regression_add_tail(self):
        self.assertEqual(self.q.size(), 0)
        self.assertEqual(self.q.get_remove_head_status(), ParentQueue.REMOVE_HEAD_NIL)
        self.assertEqual(self.q.get_get_head_status(), ParentQueue.GET_HEAD_NIL)

        for i in range(5):
            self.q.add_tail(i)
            self.assertEqual(self.q.get_head(), 0)
            self.assertEqual(self.q.get_get_head_status(), ParentQueue.GET_HEAD_OK)
            self.assertEqual(self.q.size(), i + 1)

        for i in range(7):
            if i < 5:
                self.q.remove_head()
                self.assertEqual(self.q.size(), 4 - i)
                self.assertEqual(
                    self.q.get_remove_head_status(), ParentQueue.REMOVE_HEAD_OK
                )
                continue
            with self.assertRaises(IndexError):
                self.q.remove_head()
            with self.assertRaises(IndexError):
                self.q.get_head()
            self.assertEqual(self.q.size(), 0)
            self.assertEqual(
                self.q.get_remove_head_status(), ParentQueue.REMOVE_HEAD_EMPTY
            )
            self.assertEqual(self.q.get_get_head_status(), ParentQueue.GET_HEAD_EMPTY)

        self.q.add_tail(7)
        self.assertEqual(self.q.size(), 1)
        self.assertEqual(self.q.get_head(), 7)
        self.assertEqual(self.q.get_get_head_status(), ParentQueue.GET_HEAD_OK)

    def tearDown(self):
        self.q = None


if __name__ == "__main__":
    unittest.main()
