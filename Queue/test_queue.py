import unittest

from Queue import Queue


class QueueTests(unittest.TestCase):

    def setUp(self):
        self.q = Queue()

    def test_regression_enqueue(self):
        self.assertEqual(self.q.size(), 0)
        self.assertEqual(self.q.get_dequeue_status(), Queue.DEQUEUE_NIL)
        self.assertEqual(self.q.get_first_status(), Queue.FIRST_NIL)

        for i in range(5):
            self.q.enqueue(i)
            self.assertEqual(self.q.first(), 0)
            self.assertEqual(self.q.get_first_status(), Queue.FIRST_OK)
            self.assertEqual(self.q.size(), i + 1)

        for i in range(7):
            if i < 5:
                self.q.dequeue()
                self.assertEqual(self.q.size(), 4 - i)
                self.assertEqual(self.q.get_dequeue_status(), Queue.DEQUEUE_OK)
                continue
            with self.assertRaises(IndexError):
                self.q.dequeue()
            with self.assertRaises(IndexError):
                self.q.first()
            self.assertEqual(self.q.size(), 0)
            self.assertEqual(self.q.get_dequeue_status(), Queue.DEQUEUE_EMPTY)
            self.assertEqual(self.q.get_first_status(), Queue.FIRST_EMPTY)

        self.q.enqueue(7)
        self.assertEqual(self.q.size(), 1)
        self.assertEqual(self.q.first(), 7)
        self.assertEqual(self.q.get_first_status(), Queue.FIRST_OK)

    def tearDown(self):
        self.q = None


if __name__ == "__main__":
    unittest.main()
