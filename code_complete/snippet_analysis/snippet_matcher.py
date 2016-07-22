import itertools
from fuzzywuzzy import process

# pip install fuzzywuzzy https://github.com/seatgeek/fuzzywuzzy
# TODO: Make language non-specific


class SnippetMatcher:
    """ This class matches functions based on argument type and function name

    :param snippet_analyser: A SnippetAnalyser
    :param task_arguments: The arguments required in task
    :param task_comment: The comment provided by user
    """
    def __init__(self, snippet_analyser, task_arguments, task_comment):
        self.global_types = snippet_analyser.global_type_dict
        self.all_types = snippet_analyser.type_dict
        self.snippet = snippet_analyser.snippet
        self.functions = snippet_analyser.functions
        self.helper = snippet_analyser.helper
        self.task_arguments = task_arguments            # { func1 {arg1 : type1, arg2 : type2 }, func2 ... }
        self.task_comment = task_comment
        self.matched_functions_arguments = []
        self.matched_functions_name = []
        self.matched_functions = []

    def match_functions(self):
        """ This function matches the function by argument type and argument name and orders them in decreasing
        fitting

        :return: A list of ordered matched functions
        :rtype list
        """
        if len(self.functions.keys()) == 0:
            self.populate_function_names()
        self.populate_function_arguments()
        self.match_functions_argument_name()
        self.match_functions_argument_type()

        self.matched_functions = filter(lambda x: x in self.matched_functions_arguments,
                                         [y[0] for y in self.matched_functions_name])
        return self.matched_functions

    def populate_function_names(self):
        """ This functions finds all stub_functions in the snippet

        :return: None
        """
        for key, value in self.global_types.iteritems():
            if value == 'function':
                self.functions[key] = {}

    def populate_function_arguments(self):
        """ This function populates the arguments for each stub_function in the snippet

        :return: None
        """
        for function in self.functions.keys():
            arguments = self.functions[function][1]
            temp_dict = dict()
            for argument_name in arguments.keys():
                temp_dict[argument_name] = self.all_types[argument_name]

            self.functions[function] = [self.functions[function][0], temp_dict]

    def match_functions_argument_type(self):
        """ This function populates self.matched_functions_arguments with stub_functions that fit the bill
        by argument type

        :return: None
        """
        for function in self.functions:
            all_combinations = self.match_argument_types(self.functions[function][1])
            self.functions[function] = [self.functions[function][0], self.functions[function][1], all_combinations]
            if not len(all_combinations):
                continue
            self.matched_functions_arguments.append(function)

    def match_functions_argument_name(self):
        """ This function populates self.matched_functions_name with tuples of (stub_functions, match_ratio)
         ordered by match_ratio

        :return: None
        """
        self.matched_functions_name = \
            process.extract(self.task_comment, self.functions.keys(), limit=len(self.functions.keys()))

    def match_argument_types(self, given_arguments):
        """ This function takes in a dictionary of arguments and matches it against a dictionary of task requirements,
        returning all possible valid matchings.

        For example, if given_arguments is {'x': int, 'y': int, 'z': list} and
        self.task_arguments is {'a': int, 'b': int, 'c': list}, this function will return
        [ [(x,a),(y,b),(c,z)] , [(x,b),(y,a),(c,z)] ]

        :param given_arguments: A dictionary of arguments
        :type dict

        :returns: All possible, valid matchings of given and task arguments
        :rtype: list of lists of tuples
        """

        if len(given_arguments.values()) != len(self.task_arguments.values()):
            return []

        given_arguments_list = []
        task_arguments_list = []
        for key, value in given_arguments.iteritems():
            given_arguments_list.append({key: value})
        for key, value in self.task_arguments.iteritems():
            task_arguments_list.append({key: value})

        all_combinations = list(itertools.product(given_arguments_list, task_arguments_list))

        for tup in all_combinations:
            # tup is of form ( {'x' : type}, {'a' : type} )
            if tup[0].values()[0] != tup[1].values()[0] and tup[0].values()[0] != self.helper.word_wildcard:
                all_combinations.remove(tup)

        useful_combinations = []
        one_combination = []

        for i in xrange(len(all_combinations)):
            current_first_name = all_combinations[i][0].keys()[0]
            current_second_name = all_combinations[i][1].keys()[0]

            one_combination.append([current_first_name, current_second_name])

            for j in xrange(i + 1, len(all_combinations)):
                tup = all_combinations[j]
                if tup[0].keys()[0] == current_first_name or tup[1].keys()[0] == current_second_name:
                    continue
                else:
                    one_combination.append([tup[0].keys()[0], tup[1].keys()[0]])

            if one_combination.sort() not in useful_combinations and len(one_combination) == len(given_arguments_list):
                useful_combinations.append(one_combination)
            one_combination = []

        return useful_combinations
