import unittest

from example import main_1


class TestExample(unittest.TestCase):

    def test_example_read_file(self):
        self.assertEqual(main_1(), ['1', '2', '3'])


if __name__ == '__main__':
    unittest.main()
