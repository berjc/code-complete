from snippet_analysis_helper import SnippetAnalysisHelper


class SnippetAnalyser:
    """ This class analyzes the snippets. This. This is where it all happens.

        This class takes in a snippet and figures out the scope-specific variables and their types.

        :param snippet: The code snippet to be analyzed
        :type str

        :param language_mode A LanguageMode enum to specify the language being analyzed
        """

    def __init__(self, snippet, language_mode):
        self.snippet = snippet
        self.type_dict = {}                     # This maps the words to their types in a specific scope
        self.global_type_dict = {}              # This maps the global only words to their types
        self.line_dict = {}                     # This maps the lines to their indices in the snippet
        self.snippet_word_array = [[]]          # A 2D list of all words
        self.scope_flag = 0                     # A flag to keep track of current scope level
        self.helper = SnippetAnalysisHelper(language_mode)

    def execute(self):
        """ This function prepares the inputs and then executes the needed analysis. The types are stored in type_list

        :return: None
        """
        self.prepare_data()
        self.find_types()
        self.type_dict = self.helper.clean_dict(self.type_dict)
        self.global_type_dict = self.helper.clean_dict(self.global_type_dict)
        self.helper.reset_stdout()

    def prepare_data(self):
        """ This function does the pre-analysis by preparing the data for analysis. This also populates line_dict

         :return: None
         """
        snippet = self.snippet.replace('\t', ' ')
        
        for index, line in enumerate(self.snippet.split('\n')):
            self.line_dict[index] = line

        for operator in self.helper.operators:
            snippet = snippet.replace(operator, " " + operator + " ")
            
        for unneeded_token in self.helper.unneeded_tokens:
            snippet.replace(unneeded_token, "")
            
        snippet_array = [[]]
    
        for line in snippet.split('\n'):
            snippet_array.append(line.split(" "))
            
        self.snippet_word_array = snippet_array
        
    def find_types(self):
        """ This function does the analysis of types.

         :return: None
         """
        self.scope_flag = 0
        returned = False
        
        for index, line in enumerate(self.snippet_word_array[1:]): 
            # The first element is always empty. Hence, we skip it.
            
            if line is None or len(line) <= 1:
                continue
            
            for word in line:
                if word in self.helper.scope_indicators:
                    self.scope_flag += 1
                    break
                elif word in self.helper.scope_break_indicators:
                    self.scope_flag -= 1
                    returned = True
                    break
                elif word in self.helper.ignore_flags:
                    continue
                    
            if returned:
                returned = False
                continue
                
            if self.scope_flag:
                self.find_types_helper_local_scope(line, index)
            else:
                self.find_types_helper(line)

    def find_types_helper_local_scope(self, line, index):
        """ This helper function is delegated to within local scopes
        
        :param line: The current line being considered. Code is injected AFTER the line
        :type list
        
        :param index: The index of the line inside the snippet
        :type int

        :return: None
        """
        line_as_str = self.line_dict.get(index)     # The actual, unchanged string line
        spaces = ""                                 # Indentation!
        
        for char in self.line_dict.get(index + 1): 
            if char == ' ' or char == '\t':         
                spaces += char
            else:
                break
                
        input_exec = self.snippet[:self.snippet.find(
            line_as_str)] + line_as_str + self.helper.get_local_scope_finder(spaces) + self.snippet[self.snippet.find(
                                                                                   line_as_str) + len(line_as_str):]
        output = self.helper.exec_wrapper(input_exec)
        
        if self.helper.is_global(output):    
            # We've gone to the global scope
        
            self.scope_flag -= 1
            
            if not self.scope_flag:
                self.find_types_helper(line)
            else:
                raise Exception("Something went wrong! We're in the global scope but the scope_flags are misaligned!")
        
        else:
            # We're still in local scope.
            assert self.scope_flag, "Scope flags are misaligned"
            for word in line:
                if word in self.helper.operators:
                    self.type_dict[word] = self.helper.word_operator
                else:
                    input_exec = self.snippet[:self.snippet.find(
                        line_as_str)] + line_as_str + self.helper.get_type_finder(word, spaces) + self.snippet[
                                                                                                     self.snippet.find(
                                                                                                     line_as_str) + len(
                                                                                                     line_as_str):]
                    self.find_type_from_output(input_exec, word)

    def find_types_helper(self, line):
        """ This helper function is delegated to within global scopes

        :param line: The current line being considered. Code is injected at the end of the snippet
        :type list

        :return None
        """
        for word in line:
            if word in self.helper.operators:
                self.type_dict[word] = self.helper.word_operator
            else:
                input_exec = self.snippet + self.helper.get_type_finder(word, "")
                self.find_type_from_output(input_exec, word, self.scope_flag == 0)

    def find_type_from_output(self, input_exec, word, is_global=False):
        """ This helper function is assigns types to words

        :param input_exec: The input to exec_wrapper
        :type str

        :param word: The word to assign type to
        :type str

        :param is_global: Is it a global word?
        :type bool

        :return: None
        """
        try:
            output = self.helper.exec_wrapper(input_exec)
            if output.find('Error') >= 0:
                if not self.type_dict.has_key(word) or self.type_dict[word].equals(self.helper.word_unknown):
                    self.type_dict[word] = self.helper.word_unknown
                    if is_global:
                        self.global_type_dict[word] = self.helper.word_unknown
            else:
                self.type_dict[word] = self.helper.clean_type(output)
                if is_global:
                    self.global_type_dict[word] = self.helper.clean_type(output)
        except:
            self.type_dict[word] = self.helper.word_unknown
            if is_global:
                self.global_type_dict[word] = self.helper.word_unknown

    def exec_and_print_snippet(self):
        """ This function just executes the base snippet and prints the output to stdout

         :return: None
         """
        print self.helper.exec_wrapper(self.snippet)
