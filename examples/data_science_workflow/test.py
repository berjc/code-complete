import os
import unittest

from example import open_file_and_read_all_lines
from example import convert_list_of_strings_to_ints
from example import sort_list
from example import report_median_of_list
from example import report_mean_of_list


class TestExample(unittest.TestCase):

    def test_example_open_file_and_read_all_lines(self):
        f_name = 'test_file'
        open('test_file', 'w').write('1\n2\n3\n')
        self.assertEqual(open_file_and_read_all_lines(f_name), ['1', '2', '3'])
        os.remove(f_name)

    def test_example_convert_list_of_strings_to_ints(self):
        self.assertEqual(convert_list_of_strings_to_ints(['1', '2', '3']), [1, 2, 3])

    def test_example_sort_list(self):
        self.assertEqual(sort_list([2, 3, 1]), [1, 2, 3])

    def test_example_report_median_of_list(self):
        self.assertEqual(report_median_of_list([1, 2, 3, 4, 1000]), 'Median: %d' % 3)

    def test_example_report_mean_of_list(self):
        self.assertEqual(report_mean_of_list([1, 2, 3, 4, 1000]), 'Mean: %f' % 202)


if __name__ == '__main__':
    unittest.main()
