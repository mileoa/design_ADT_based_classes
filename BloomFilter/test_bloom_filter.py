import random
import unittest
import uuid

from BloomFilter import BloomFilter


class BloomFilterTests(unittest.TestCase):

    def setUp(self):
        self.bf = BloomFilter(32, 99.0)
        self.test_strings = [
            "0123456789",
            "1234567890",
            "2345678901",
            "3456789012",
            "4567890123",
            "5678901234",
            "6789012345",
            "7890123456",
            "8901234567",
            "9012345678",
        ]

    def test_regression_is_value(self):
        for s in self.test_strings:
            self.assertFalse(self.bf.is_value(s))

        self.bf.add(self.test_strings[0])
        self.assertTrue(self.bf.is_value(self.test_strings[0]))

    def test_regression_random(self):
        for i in range(1000):
            input_amount = random.randint(1, 100)
            accuracy = random.randint(1, 9999) / 100
            bf = BloomFilter(input_amount, accuracy)

            strings = [uuid.uuid4() for _ in range(input_amount)]

            for string in strings:
                bf.add(string)
                self.assertTrue(bf.is_value(string))

    def test_accuracy(self):
        input_amount = 100000
        accuracy = 87.4
        bf = BloomFilter(input_amount, accuracy)

        exist_strings = [uuid.uuid4() for _ in range(input_amount // 2)]
        not_exist_strings = [uuid.uuid4() for _ in range(input_amount // 2)]

        for string in exist_strings:
            bf.add(string)

        false_positive_amount = 0
        for string in not_exist_strings:
            if bf.is_value(string):
                false_positive_amount += 1
        false_positive_percent = 100 * false_positive_amount / input_amount
        self.assertLessEqual(false_positive_percent, 100 - accuracy)

    def tearDown(self):
        del self.bf
        del self.test_strings


if __name__ == "__main__":
    unittest.main()
