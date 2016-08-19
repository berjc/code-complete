import unittest

from example import main_1
from example import main_2
from example import main_3
from example import main_4


class TestExample(unittest.TestCase):

    def test_example_add(self):
        self.assertEqual(main_1(), 3)

    def test_example_multiply(self):
        self.assertEqual(main_2(), 56)

    def test_example_subtract(self):
        self.assertEqual(main_3(), -1)

    def test_example_divide(self):
        self.assertEqual(main_4(), 41)


if __name__ == '__main__':
    unittest.main()
