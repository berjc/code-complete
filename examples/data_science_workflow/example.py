# Data Science Workflow


def read_file_lines_stripped(f):
    """
    Read all lines of a file, and remove trailing and leading whitespace
    """
    with open(f) as f:
        return map(lambda x: x.strip(), f.readlines())


def convert_to_int_list(string_list):
    """
    Return a list of integers
    :param string_list: List of Ints as Strings
    :return: List of Ints
    """
    return list(map(int, string_list))


def bubble_sort(in_list_to_sort):
    """ (List) -> List
    This function will take a list of random integers and then apply bubble
    sort on it.  It will return a sorted list of numbers.
    """
    list_is_sorted = False

    while (list_is_sorted is False):
        list_is_sorted = True  # Default to True... and set it to False if we make a swap
        i = 0

        while (i < len(in_list_to_sort) - 1):
            if (in_list_to_sort[i] > in_list_to_sort[i + 1]):
                temp_num = in_list_to_sort[i + 1]
                in_list_to_sort[i + 1] = in_list_to_sort[i]
                in_list_to_sort[i] = temp_num

                list_is_sorted = False

            i += 1

    return in_list_to_sort


def median(list_of_int):
    retval = None
    list_len = len(list_of_int)

    # sort the list
    list_of_int.sort()

    # if list has even num, find average of middle two
    if list_len % 2 == 0:
        a = list_of_int[int(list_len / 2 - 1)]
        b = list_of_int[int(list_len / 2)]

        retval = (a + b) / 2.0

    # else get median
    else:
        retval = list_of_int[int(round(list_len / 2))]

    return retval


def mean(vals=[]):
    """
    Calculates the mean values of a list of numbers
    If you enter a list of ints, you'll get a list of ints!!

    RETURNS
    mean value of list
    """
    # mean_val = sum(vals)/float(len(vals))
    mean_val = sum(vals) / len(vals)
    return mean_val


def open_file_and_read_all_lines(f_name):
    l = read_file_lines_stripped(f_name)
    return l


def convert_list_of_strings_to_ints(l):
    l = convert_to_int_list(l)
    return l


def sort_list(l):
    l = bubble_sort(l)
    return l


def report_median_of_list(l):
    z = median(l)
    return 'Median: %d' % z


def report_mean_of_list(l):
    z = mean(l)
    return 'Mean: %f' % z


if __name__ == '__main__':
    # Setup File
    f_name = 'test_file'
    open('test_file', 'w').write('30\n50\n10\n100\n80\n')

    lines = open_file_and_read_all_lines(f_name)
    int_lines = convert_list_of_strings_to_ints(lines)
    sorted_ints = sort_list(int_lines)
    print report_median_of_list(sorted_ints)
    print report_mean_of_list(sorted_ints)
