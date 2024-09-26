import re

from constants import CLOSING_BRACKETS, CONSTANT, FUNCTION, OPENING_BRACKETS, OPERATION_SIGN, UNARY_SIGN, UNRECOGNIZED, VARIABLE

class Lexer:
    FUNC_PATTERN = r'(sin|cos|tg|ctg|log|func)'
    OPENING_BRACKET = '('
    CLOSING_BRACKET = ')'
    UNARY = '-'
    OPERATORS = '+*/'
    SEPARATOR = '.'

    def __init__(self, input_text):
        self.text = input_text
        self.position = 0
        self.curr_state = self.text[self.position] 
        self.tokens = []
        self.func_pattern = re.compile(self.FUNC_PATTERN)
        self.is_end = False

    def next(self):
        self.position += 1
        if self.position < len(self.text):
            self.curr_state = self.text[self.position]
        else:
            self.is_end = True

    def number(self):
        number = ''
        decimal_point_count = 0
        while not self.is_end and (self.curr_state.isdigit() or (self.curr_state == self.SEPARATOR and decimal_point_count == 0)):
            if self.curr_state == self.SEPARATOR:
                decimal_point_count += 1
            number += self.curr_state
            self.next()
        if decimal_point_count > 1:
            self.tokens.append((UNRECOGNIZED, number))  
        else:
            self.tokens.append((CONSTANT, number))  
        return (CONSTANT, number)  
    
    def variable(self, char):
        self.tokens.append((VARIABLE, char))

    def mat_function(self):
        func_match =  self.func_pattern.match(self.text[self.position:])
        if func_match:
            func = func_match.group(0)
            self.position += len(func) - 1 
            self.next()  
            return (FUNCTION, func)
        return None

    def identifier(self):
        func_token = self.mat_function()
        if func_token:
            self.tokens.append(func_token)  
            if not self.is_end and self.curr_state.isalpha():
                self.variable(self.curr_state) 
                self.next()
            return func_token
        
        self.variable(self.curr_state)
        self.next()
    
    def brackets(self):
        if self.curr_state == self.OPENING_BRACKET:
            self.next()
            self.tokens.append((OPENING_BRACKETS, self.OPENING_BRACKET))
        
        if self.curr_state == self.CLOSING_BRACKET:
            self.next()
            self.tokens.append((CLOSING_BRACKETS, self.CLOSING_BRACKET))

    def operator(self):
        if self.curr_state == self.UNARY:
            char = self.curr_state
            self.next()
            token = (UNARY_SIGN if (len(self.tokens) == 0 or self.tokens[-1][0] in {OPERATION_SIGN, OPENING_BRACKETS}) else OPERATION_SIGN, char)
            self.tokens.append(token)
        
        if self.curr_state in self.OPERATORS:
            char = self.curr_state
            self.next()
            self.tokens.append((OPERATION_SIGN, char))

    def handle_unrecognized(self):
        char = self.curr_state
        self.next() 
        self.tokens.append((UNRECOGNIZED, char))

    def lexical_analysis(self):       
        if self.curr_state.isalpha():
            return self.identifier()

        if self.curr_state.isdigit():
            return self.number()

        if self.curr_state in self.OPERATORS + self.UNARY:
            return self.operator()
        
        if self.curr_state in self.OPENING_BRACKET + self.CLOSING_BRACKET:
            return self.brackets()
        
        self.handle_unrecognized()
