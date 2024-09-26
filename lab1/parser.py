from constants import CLOSING_BRACKETS, CONSTANT, END, FUNCTION, OPENING_BRACKETS, OPERATION_SIGN, START, UNARY_SIGN, VARIABLE

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.ob_positions = []
        self.errors = []
        self.transitions = {
            START: [UNARY_SIGN, FUNCTION, OPENING_BRACKETS, VARIABLE, CONSTANT],
            UNARY_SIGN: [FUNCTION, OPENING_BRACKETS, VARIABLE, CONSTANT],
            FUNCTION: [OPENING_BRACKETS],
            OPENING_BRACKETS: [VARIABLE, CONSTANT, UNARY_SIGN, OPENING_BRACKETS, FUNCTION],
            VARIABLE: [OPERATION_SIGN, CLOSING_BRACKETS],
            CONSTANT: [OPERATION_SIGN, CLOSING_BRACKETS],
            CLOSING_BRACKETS: [OPERATION_SIGN, CLOSING_BRACKETS],
            OPERATION_SIGN: [FUNCTION, OPENING_BRACKETS, VARIABLE, CONSTANT],
            END: [CONSTANT, VARIABLE, CLOSING_BRACKETS]
        }

    def add_error(self, message, position=None):
        if position is None:
            position = self.position
        self.errors.append(f"Error at position {position}: {message}")
    
    def print_result(self):
        if self.errors:
            for error in self.errors:
                print(error)
        else:
            print("Errors not found.")

    def parse(self):
        curr_state = START
        brackets_count = 0

        while self.position < len(self.tokens):
            token_type, _ = self.tokens[self.position]

            if token_type == OPENING_BRACKETS:
                brackets_count += 1
                self.ob_positions.append(self.position)

            elif token_type == CLOSING_BRACKETS:
                brackets_count -= 1
                if brackets_count < 0:
                    self.add_error("unmatched closing bracket")
                    brackets_count = 0

            if token_type == CLOSING_BRACKETS and (self.position == 0 or self.tokens[self.position - 1][0] in {OPENING_BRACKETS, OPERATION_SIGN}):
                self.add_error("empty brackets")

            if token_type not in self.transitions:
                self.add_error(f"unexpected token '{token_type}'")
                self.position += 1
                continue

            if token_type not in self.transitions.get(curr_state, []):
                self.add_error(f"unexpected token '{token_type}' in state '{curr_state}'")
                curr_state = token_type  
                self.position += 1
                continue

            curr_state = token_type
            self.position += 1

        if brackets_count > 0:
            position = self.ob_positions[-1]
            self.add_error("unmatched opening bracket", position)
        elif curr_state not in self.transitions[END]:
            self.add_error(f"unexpected token '{token_type}' at the end of the expression")

        self.print_result()
    