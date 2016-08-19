import unittest

from example import main_1


class TestExample(unittest.TestCase):

    def test_example_sort_list(self):
        self.assertEqual(main_1(), ['A', 'B', 'C'])


if __name__ == '__main__':
    unittest.main()
