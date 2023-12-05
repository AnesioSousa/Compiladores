"""
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id

"""


class LL1Parser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.index = 0
        self.current_token = None

    def parse(self):
        self.current_token = self.get_next_token()
        self.parse_E()

    def get_next_token(self):
        if self.index < len(self.input_string):
            token = self.input_string[self.index]
            self.index += 1
            return token
        else:
            return None

    def match(self, expected_token):
        if self.current_token == expected_token:
            self.current_token = self.get_next_token()
        else:
            raise Exception(
                f"Error: Expected {expected_token}, got {self.current_token}")

    def parse_E(self):
        self.parse_T()
        self.parse_E_prime()

    def parse_E_prime(self):
        if self.current_token == '+':
            self.match('+')
            self.parse_T()
            self.parse_E_prime()
        else:
            pass  # E' -> ε

    def parse_T(self):
        self.parse_F()
        self.parse_T_prime()

    def parse_T_prime(self):
        if self.current_token == '*':
            self.match('*')
            self.parse_F()
            self.parse_T_prime()
        else:
            pass  # T' -> ε

    def parse_F(self):
        if self.current_token == '(':
            self.match('(')
            self.parse_E()
            self.match(')')
        elif self.current_token.isalpha():
            self.match(self.current_token)
        else:
            raise Exception(f"Error: Unexpected token {self.current_token}")


# Example usage
input_string = "(E)"
parser = LL1Parser(input_string)
parser.parse()
print("Parsing successful.")
