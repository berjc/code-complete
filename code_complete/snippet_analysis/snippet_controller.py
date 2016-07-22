from snippet_analyser import SnippetAnalyser
from snippet_matcher import SnippetMatcher
from snippet_analysis_helper import LanguageMode
import os


class SnippetController:
    def __init__(self, snippet, task_arguments, task_comment, language_mode=LanguageMode.python, debug=False):
        self.task_arguments = task_arguments
        self.task_comment = task_comment
        self.snippet = snippet
        self.snippet_analyser = SnippetAnalyser(snippet, language_mode)
        self.snippet_matcher = None
        self.debug = debug

    def analyze(self):
        self.snippet_analyser.execute()
        self.snippet_matcher = SnippetMatcher(self.snippet_analyser,
                                              self.task_arguments,
                                              self.task_comment)
        self.snippet_matcher.match_functions()

        if self.debug:
            print "Global types"
            print self.snippet_analyser.global_type_dict
            print "Local unique types"
            print self.snippet_analyser.type_dict
            print "==========="
            print "Matched Functions"
            print self.snippet_matcher.match_functions()
            print "Detailed Function Info"
            print self.snippet_matcher.functions

    def clean(self):
        to_clean = [self.snippet_analyser.helper.filename[:-3],
                    self.snippet_analyser.helper.filename + "c", self.snippet_analyser.helper.filename]
        for temp_file in to_clean:
            try:
                os.remove(temp_file)
            except OSError:
                pass

    def find_snippet(self):
        self.analyze()
        self.clean()
        return self.snippet_matcher.match_functions(), self.snippet_matcher.functions

if __name__ == "__main__":
    snippet = """
def concat_string(x,y):
    return x+y

def add_two_numbers(a,b):
    return a+b

def subtract_two_numbers(c,d):
    return c-d

def sort_a_list(u_list):
    return u_list.sort()

print "hello"
"""
    sc = SnippetController(snippet, {'a1': 'int', 'b1': 'int'}, "subtract two numbers", LanguageMode.python, True)
    sc.analyze()
    sc.clean()
