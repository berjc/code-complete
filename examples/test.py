import unittest
import example


class TestExample(unittest.TestCase):

    def test_example_add(self):
        self.assertEqual(example.main_1(), 3)

    def test_example_multiply(self):
        self.assertEqual(example.main_2(), 2)

if __name__ == '__main__':
    unittest.main()
