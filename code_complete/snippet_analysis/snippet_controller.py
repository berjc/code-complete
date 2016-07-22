from snippet_analyser import SnippetAnalyser
from snippet_matcher import SnippetMatcher
from snippet_analysis_helper import LanguageMode


class SnippetController:
    def __init__(self, snippet, task_arguments, task_comment, language_mode=LanguageMode.python):
        self.task_arguments = task_arguments
        self.task_comment = task_comment
        self.snippet = snippet
        self.snippet_analyser = SnippetAnalyser(snippet, language_mode)
        self.snippet_matcher = None

    def analyze(self):
        self.snippet_analyser.execute()
        self.snippet_matcher = SnippetMatcher(self.snippet_analyser.global_type_dict,
                                              self.snippet_analyser.type_dict,
                                              self.snippet,
                                              self.task_arguments,
                                              self.task_comment)
        print self.snippet_analyser.global_type_dict
        print self.snippet_analyser.type_dict
        print self.task_arguments
        print "==========="
        print self.snippet_matcher.match_functions()


if __name__ == "__main__":
    snippet = """
def concat_string(x,y):
    return x+y

def add_two_numbers(a,b):
    return a+b

def sort_a_list(u_list):
    return u_list.sort()

print concat_string("hello "," world")
print add_two_numbers(3,4)
print sort_a_list([0, 4, 3])
"""
    sc = SnippetController(snippet, {'mylist': 'list'}, "sort a list", LanguageMode.python)
    sc.analyze()
