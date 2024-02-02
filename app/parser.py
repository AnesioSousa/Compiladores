"""
Universidade Estadual de Feira de Santana
EXA869 - MI - PROCESSADORES DE LINGUAGEM DE PROGRAMAÇÃO - TP02 - 2023.2
Autor: Anésio Neto 
Docente: Matheus Pires
"""


class GoatParser:
    """
    Classe que possibilita a criação de objetos
    capazes de gerar árvores sintáticas partindo de tokens de entrada.
    """

    """
    def __init__(self, file_name, input_sequence=[]):
        self._file_name = file_name
        self._input_sequence = input_sequence
        self._lookahead = self._input_sequence[0]
        self._token_counter = 0
        self._output = open(f'./files/{file_name}-saida.txt', 'a', encoding='utf-8')
    """

    def __init__(self, input_sequence):
        self._input_sequence = input_sequence
        self._lookahead = self._input_sequence[0]
        self._token_counter = 0

    def program(self):
        if self._lookahead['lexeme'] == 'const':
            self.constant_block()
            if self._lookahead['lexeme'] == 'variables':
                self.variable_block()
                if self._lookahead['lexeme'] == 'class':
                    self.class_block()
                    if self._lookahead['lexeme'] == 'objects':
                        self.object_block()
                        if self._lookahead['lexeme'] == 'class':
                            self.main_class()
        return True

    def error(self):
        sync_tokens = [';']
        # self._output.write(f"Syntax Error: Found: '{self._lookahead['lexeme']}', number_line: {self._lookahead['number_line']}\n")

        while (self._lookahead['lexeme'] not in sync_tokens):
            self._lookahead = self.next_token()
            if (self._token_counter == len(self._input_sequence)-1):
                break
        self._lookahead = self.next_token()

    def variable_block(self):
        self.match('variables')
        if self._lookahead['lexeme'] == '{':
            self.match('{')
            self.variable()
            if self._lookahead['lexeme'] == '}':
                self.match('}')
            else:
                return False

        # print("Variables read successfully")

    def number_list(self):
        if self._lookahead['token_type'] == 'NRO':
            self.match(self._lookahead['lexeme'])
            if self._lookahead['lexeme'] == ',':
                self.match(',')
                self.number_list()
        else:
            self.error()

    def tre(self):
        if self._lookahead['lexeme'] == '[':
            self.match('[')
            self.number_list()
            if self._lookahead['lexeme'] == ']':
                self.match(']')
                if self._lookahead['lexeme'] == ',':
                    self.match(',')
                    self.tre()

    def variable(self):
        if self._lookahead['lexeme'] in ['int', 'real', 'string']:
            self.match(self._lookahead['lexeme'])
            self.dimension()
            if self.ide():
                if self._lookahead['lexeme'] == '=':
                    self.match('=')
                    if self._lookahead['token_type'] in ['NRO', 'CAC', 'IDE']:
                        self.assignment_value()

                    # Será que eu to limitando a abertura só de até duas chaves '[['?
                    elif self._lookahead['lexeme'] == '[':
                        self.array()
                    else:
                        return self.error()
            else:
                return self.error()
            self.variable_end()
        elif self._lookahead['lexeme'] == 'boolean':
            self.match(self._lookahead['lexeme'])
            if self.ide():
                # OPTIONAL VALUE TAMBÉM DEIXA ATRIBUIR ARRAYS PARA VARIAVEIS DOS TIPOS STRING E BOOLEAN!
                self.optional_value()
                self.variable_end()

    def variable_end(self):
        self.variable_same_line()
        if self._lookahead['lexeme'] == ';':
            self.match(';')
            self.variable()
        else:
            self.error()

    def for_init(self):
        if self._lookahead['lexeme'] == '=':
            self.match('=')
            return self.check_for_int()
        else:
            return False

    def check_for_int(self):
        lexeme = self._lookahead['lexeme']
        try:
            int(lexeme)

            # Se a conversão for bem-sucedida, significa que é um número inteiro
            self.match(lexeme)
            return True
        except ValueError:
            # Se a conversão falhar, significa que não é um número inteiro
            # Adicione aqui qualquer tratamento adicional desejado
            self._output.write(
                f"Syntax Error: The for statement initialization needs to be an integer! Found: '{self._lookahead['lexeme']}', number_line: {self._lookahead['number_line']}\n")
            self.error()

        return False

    def variable_same_line(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            self.ide()
            self.optional_value()
            self.variable_same_line()

    def optional_value(self):
        if self._lookahead['lexeme'] == '=':
            self.match('=')
            self.assignment_value()
        else:
            return False

    def assignment_value(self):
        if self.ide():
            self.object_value()
        elif self.value():
            return True
        elif self._lookahead['lexeme'] == '[':
            self.array()
            return True

        return False

    def match(self, symbol):
        if symbol == self._lookahead['lexeme']:
            self._lookahead = self.next_token()
            return True
        else:
            # print(f"expected {symbol}, found {self._lookahead['lexeme']}\n")
            return False

    def next_token(self):
        if (self._token_counter < len(self._input_sequence)-1):
            self._token_counter += 1
        return self._input_sequence[self._token_counter]

    def constant_block(self):
        self.match('const')
        if self._lookahead['lexeme'] == '{':
            self.match('{')
            if self.constant():
                if self._lookahead['lexeme'] == '}':
                    self.match('}')
            else:
                return False
        # print('Const read sucessfully')

        return True

    def constant(self):
        if self.type():
            if self.ide():
                if self._lookahead['lexeme'] == '=':
                    self.match('=')
                    if self.assignment_value() and self.constant_same_line():
                        if self._lookahead['lexeme'] == ';':
                            self.match(';')
                            return self.constant()
        elif self._lookahead['lexeme'] == '}':
            return True

        return False

    def assignment_value(self):
        if self.ide():
            if self._lookahead['lexeme'] == '.':
                self.object_value()
                return True
            elif self.access_expression():
                return True
        elif self.value():
            return True
        elif self._lookahead['lexeme'] == '[':
            self.array()
            return True

        return False

    def constant_same_line(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            if self.ide():
                if self._lookahead['lexeme'] == '=':
                    self.match('=')
                    return self.assignment_value() and self.constant_same_line()
        else:
            return True
        # Rever isso aqui!
        return False

    def ide(self):
        if self._lookahead['token_type'] == 'IDE':
            self.match(self._lookahead['lexeme'])
            return True
        return False

    def type(self):
        if self._lookahead['lexeme'] in ['int', 'string', 'boolean', 'real', 'void']:
            self.A()
            if self._lookahead['lexeme'] in ['[']:
                self.dimension()

            return True

        return False

    def A(self):
        if self._lookahead['lexeme'] == 'int':
            self.match('int')
        elif self._lookahead['lexeme'] == 'string':
            self.match('string')
        elif self._lookahead['lexeme'] == 'boolean':
            self.match('boolean')
        elif self._lookahead['lexeme'] == 'real':
            self.match('real')
        elif self._lookahead['lexeme'] == 'void':
            self.match('void')
        else:
            return False  # ERRO

    def dimension(self):
        if self._lookahead['lexeme'] in ['[']:
            self.match('[')
            # Tá permitindo float na inicialização?
            self.number()
            if self._lookahead['lexeme'] in [']']:
                self.match(']')
                self.dimension()

    def array(self):
        if self._lookahead['lexeme'] == '[':
            self.match('[')
            if self._lookahead['lexeme'] == '[':
                self.tre()
            else:
                self.number_list()

            if self._lookahead['lexeme'] == ']':
                self.match(']')
            else:
                return self.error()

    def array_value(self):
        self.possible_value()
        self.more_array_value()

    def object_value(self):
        if self._lookahead['lexeme'] == '.':
            self.match('.')
            self.ide()

    def value(self):
        if self._lookahead['token_type'] == 'NRO':
            return self.number()
        elif self._lookahead['token_type'] == 'CAC':
            return self.match(self._lookahead['lexeme'])
        elif self._lookahead['token_type'] == 'IDE':
            return self.ide()
        # Rever isso!
        elif self._lookahead['lexeme'] in ['true', 'false']:
            return self.match(self._lookahead['lexeme'])
        return False

    def number(self):
        if self._lookahead['token_type'] == 'NRO':
            self.match(self._lookahead['lexeme'])
            return True

        return False

    def possible_value(self):
        if self.ide():
            self.object_value()
        # lembrar do porém da token ser boolean acima!
        elif self._lookahead['token_type'] in ['NRO', 'CAC', 'IDE']:
            self.value()
        elif self._lookahead['lexeme'] == '[':
            self.array()
            self.more_array_value()
            self.match(']')

    def main_class(self):
        self.match('class')
        if self._lookahead['lexeme'] == 'main':
            self.match('main')
            if self._lookahead['lexeme'] == '{':
                self.match('{')
                ans = self.main_class_content()
                if self._lookahead['lexeme'] == '}':
                    self.match('}')
                    # print("Main class content was read successfully")
                    return ans

        return False

    def main_class_content(self):
        self.statement_sequence()

    def object_block(self):
        if self._lookahead['lexeme'] == 'objects':
            self.match('objects')
            if self._lookahead['lexeme'] == '{':
                self.match('{')
                self.object()
                if self._lookahead['lexeme'] == '}':
                    self.match('}')
                    # print("Object block was read successfully")
                    return True
                else:
                    return False
            else:
                return False

    def object(self):
        if self.ide():
            if self.ide():
                if self._lookahead['lexeme'] == '=':
                    self.match('=')
                    if self.ide():
                        if self._lookahead['lexeme'] == '->':
                            self.match('->')
                            if self._lookahead['lexeme'] == 'constructor':
                                self.match('constructor')
                                if self._lookahead['lexeme'] == '(':
                                    self.match('(')
                                    self.args_list()
                                    if self._lookahead['lexeme'] == ')':
                                        self.match(')')
                                        self.object_same_line()
                                        if self._lookahead['lexeme'] == ';':
                                            self.match(';')
                                            self.object()
                                        else:
                                            return False
                                    else:
                                        return False

        return True

    def object_same_line(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            if self.ide():
                if self._lookahead['lexeme'] == '=':
                    self.match('=')
                    if self.ide():
                        if self._lookahead['lexeme'] == '->':
                            self.match('->')
                            if self._lookahead['lexeme'] == 'constructor':
                                self.match('constructor')
                                if self._lookahead['lexeme'] == '(':
                                    self.match('(')
                                    self.args_list()
                                    if self._lookahead['lexeme'] == ')':
                                        self.match(')')

    def statement_sequence(self):
        if self._lookahead['lexeme'] in ['if', 'for', 'pass']:
            self.statement()
            self.statement_sequence()
        elif self._lookahead['lexeme'] in ['print', 'read']:
            self.command()
            self.statement_sequence()
        elif self.expression_sequence():
            self.statement_sequence()

    def statement(self):
        if self.if_statement():
            return True
        elif self.for_statement():
            return True
        elif self._lookahead['lexeme'] == 'pass':
            return True

        return False

    def if_statement(self):
        if self._lookahead['lexeme'] == 'if':
            self.match('if')
            if self.condition():
                if self._lookahead['lexeme'] == 'then':
                    self.match('then')
                    if self._lookahead['lexeme'] == '{':
                        self.match('{')
                        self.statement_sequence()
                        if self._lookahead['lexeme'] == '}':
                            self.match('}')
                            self.else_statement()
                            return True
                        else:
                            return False

    def else_statement(self):
        if self._lookahead['lexeme'] == 'else':
            self.match('else')
            if self._lookahead['lexeme'] == '{':
                self.match('{')
                self.statement_sequence()
                if self._lookahead['lexeme'] == '}':
                    self.match('}')
                    return True

        return False

    def condition(self):
        if self._lookahead['lexeme'] == '(':
            self.match('(')
            if self.logical_and_expression():
                if self._lookahead['lexeme'] == ')':
                    self.match(')')
                    return True

        return False

    def logical_and_expression(self):
        if self.logical_or_expression():
            self.logical_and_expression_alt()
            return True

        return False

    def logical_and_expression_alt(self):
        if self._lookahead['lexeme'] == '&&':
            self.match("&&")
            if self.logical_or_expression():
                self.logical_and_expression_alt()
                return True

    def logical_or_expression(self):
        if self.logical_not_expression():
            self.logical_or_expression_alt()
            return True
        elif self._lookahead['lexeme'] == '(':
            self.match('(')
            if self.logical_or_expression():
                if self._lookahead['lexeme'] == ')':
                    self.match(')')
                    self.logical_or_expression_alt()
                    return True

    def logical_or_expression_alt(self):
        if self._lookahead['lexeme'] == '||':
            self.match('||')
            if self.logical_not_expression():
                self.logical_or_expression_alt()
                return True

        return True

    def logical_or_expression(self):
        if self.logical_not_expression():
            self.logical_or_expression_alt()
            return True
        elif self._lookahead['lexeme'] == '(':
            self.match('(')
            self.logical_or_expression()
            if self._lookahead['lexeme'] == ')':
                self.match(')')
                self.logical_or_expression_alt()
                return True

        return False

    def logical_not_expression(self):
        if self.equality_expression():
            return True
        elif self._lookahead['lexeme'] == '!':
            self.match('!')
            return self.logical_not_expression()

        return False

    def equality_expression(self):
        if self.relational_expression():
            self.equality_expression_list()
            return True
        return False

    def equality_expression_list(self):
        if self._lookahead['lexeme'] == '!=':
            self.match('!=')
            return self.relational_expression()
        elif self._lookahead['lexeme'] == '==':
            self.match('==')
            return self.relational_expression()

        return True

    def relational_expression(self):
        if self.additive_expression():
            self.relational_expression_list()
            return True

        return False

    def relational_expression_list(self):
        if self._lookahead['lexeme'] == '<':
            self.match('<')
            return self.additive_expression()
        elif self._lookahead['lexeme'] == '>':
            self.match('>')
            return self.additive_expression()
        elif self._lookahead['lexeme'] == '<=':
            self.match('<=')
            return self.additive_expression()
        elif self._lookahead['lexeme'] == '>=':
            self.match('>=')
            return self.additive_expression()

    def for_statement(self):
        if self._lookahead['lexeme'] == 'for':
            self.match('for')
            if self._lookahead['lexeme'] == '(':
                self.match('(')
                self.variable()
                self.logical_and_expression()
                if self._lookahead['lexeme'] == ';':
                    self.match(';')
                    if self.unary_expression():
                        if self._lookahead['lexeme'] == ')':
                            self.match(')')
                            if self._lookahead['lexeme'] == '{':
                                self.match('{')
                                self.statement_sequence()
                                if self._lookahead['lexeme'] == '}':
                                    self.match('}')
                                    return True
        return False

    def unary_expression(self):
        if self.access_expression():
            self.unary_expression_list()
            return True

        return False

    def access_expression(self):
        if self.primary_expression():
            return True
        elif self.access_expression_list():
            return True

        return False

    def primary_expression(self):
        if self.ide():
            return True
        elif self.number():
            return True
        elif self.bool():
            return True
        elif self.str():
            return True
        elif self.method_call():
            return True

        return False

    def method_call(self):
        if self.ide():
            if self._lookahead['lexeme'] == '(':
                self.match('(')
                self.args_list()
                if self._lookahead['lexeme'] == ')':
                    self.match(')')
                    return True

        return False

    def args_list(self):
        self.assignment_value()
        self.assignment_value_list()
        return True

    def assignment_value_list(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            self.args_list()

    # Rever isso: Const analisa strings sem precisar disso!
    def str(self):
        return True if self._lookahead['token_type'] == 'CAC' else False

    def bool(self):
        return True if self._lookahead['lexeme'] == 'true' or self._lookahead['lexeme'] == 'false' else False

    def access_expression_list(self):
        if self._lookahead['lexeme'] == '->':
            self.match('->')
            return self.primary_expression()
        elif self._lookahead['lexeme'] == '.':
            self.match('.')
            return self.primary_expression()
        elif self._lookahead['lexeme'] == '[':
            self.match('[')
            if self.primary_expression():
                if self._lookahead['lexeme'] == ']':
                    self.match(']')
                    return True

    def unary_expression_list(self):
        if self._lookahead['lexeme'] == '++':
            self.match('++')
        if self._lookahead['lexeme'] == '--':
            self.match('--')

    def multiplicative_expression(self):
        if self.unary_expression():
            self.multiplicative_expression_list()
            return True
        return False

    def multiplicative_expression_list(self):
        if self._lookahead['lexeme'] == '*':
            self.match('*')
            return self.unary_expression()
        elif self._lookahead['lexeme'] == '/':
            self.match('/')
            return self.unary_expression()

        return True

    # Tirei o "if self.type():" antes do "if self.ide():"
    def parameter(self):
        if self.ide():
            self.parameter_value_list()

        return True

    def parameter_value_list(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            self.parameter()

    def class_block(self):
        if self._lookahead['lexeme'] == 'class':
            self.match('class')
            if self.ide():
                self.class_extends()
                if self._lookahead['lexeme'] == '{':
                    self.match('{')
                    self.class_content()
                    if self._lookahead['lexeme'] == '}':
                        self.match('}')
                        self.class_block()
                        # print("Class block was read successfully")

    def class_extends(self):
        if self._lookahead['lexeme'] == 'extends':
            self.match('extends')
            if not self.ide():
                return False

        return True

    def class_content(self):
        self.variable_block()
        self.constructor()
        self.methods()

    def constructor(self):
        if self._lookahead['lexeme'] == 'constructor':
            self.match('constructor')
            if self._lookahead['lexeme'] == '(':
                self.match('(')
                self.parameter()
                if self._lookahead['lexeme'] == ')':
                    self.match(')')
                    if self._lookahead['lexeme'] == '{':
                        self.match('{')
                        self.assignment_method()
                        if self._lookahead['lexeme'] == '}':
                            self.match('}')
                            return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        return True

    def assignment_method(self):
        if self._lookahead['lexeme'] == 'this':
            self.match('this')
            if self._lookahead['lexeme'] == '.':
                self.match('.')
                if self.ide():
                    self.optional_value()
                    if self._lookahead['lexeme'] == ';':
                        self.match(';')
                        self.assignment_method()

    def additive_expression(self):
        if self.multiplicative_expression():
            return True
        elif self.additive_expression_list():
            return True

        return False

    def additive_expression_list(self):
        if self._lookahead['lexeme'] == '+':
            self.match('+')
            return self.multiplicative_expression()
        elif self._lookahead['lexeme'] == '-':
            self.match('-')
            return self.multiplicative_expression()

        return False

    def ide_list(self):
        if self.ide():
            return self.ide_lis_list()

    def ide_lis_list(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            return self.ide_list()

        return True

    def declaration_expression(self):
        if self.type():
            return self.ide_list()

    def assignment_expression(self):
        if self.type():
            if self.ide():
                if self._lookahead['lexeme'] == '=':
                    self.match('=')
                    return self.logical_and_expression()
        elif self.ide():
            if self._lookahead['lexeme'] == '=':
                self.match('=')
                return self.logical_and_expression()

        return False

    def expression(self):
        if self.declaration_expression():
            return True
        elif self.assignment_expression():
            return True

        return False

    def expression_sequence(self):
        if self.expression():
            if self._lookahead['lexeme'] == ';':
                self.match(';')
                self.expression_sequence_list()
                return True

    # Rever esse método. Uma parte está só comentada na gramática
    def expression_sequence_list(self):
        if self.expression_sequence():
            return True

        return True

    def assignment_expression(self):
        if self.type():
            if self.ide():
                if self._lookahead['lexeme'] == '=':
                    self.match('=')
                    return self.logical_and_expression()
        elif self.ide():
            if self._lookahead['lexeme'] == '=':
                self.match('=')
                return self.logical_and_expression()

        return False

    def print_command(self):
        if self._lookahead['lexeme'] == 'print':
            self.match('print')
            if self._lookahead['lexeme'] == '(':
                self.match('(')
                self.possible_value()
                if self._lookahead['lexeme'] == ')':
                    self.match(')')
                    if self._lookahead['lexeme'] == ';':
                        self.match(';')
                        return True
        else:
            return False

    def read_command(self):
        if self._lookahead['lexeme'] == 'read':
            self.match('read')
            if self._lookahead['lexeme'] == '(':
                self.match('(')
                if self.ide():
                    self.object_value()
                    if self._lookahead['lexeme'] == ')':
                        self.match(')')
                        if self._lookahead['lexeme'] == ';':
                            self.match(';')
                            return True

        return False

    def command(self):
        if self.print_command():
            return True
        elif self.read_command():
            return True

        return False

    def methods(self):
        if self._lookahead['lexeme'] == 'methods':
            self.match('methods')
            if self._lookahead['lexeme'] == '{':
                self.match('{')
                self.method()
                if self._lookahead['lexeme'] == '}':
                    self.match('}')

    def method(self):
        if self.type():
            if self.ide():
                if self._lookahead['lexeme'] == '(':
                    self.match('(')
                    self.parameter()
                    if self._lookahead['lexeme'] == ')':
                        self.match(')')
                        if self._lookahead['lexeme'] == '{':
                            self.match('{')
                            self.statement_sequence()
                            if self._lookahead['lexeme'] == 'return':
                                self.match('return')
                                if self.value():
                                    if self._lookahead['lexeme'] == ';':
                                        self.match(';')
                                        if self._lookahead['lexeme'] == '}':
                                            self.match('}')
                            elif self._lookahead['lexeme'] == '}':
                                self.match('}')
                            self.method()


if __name__ == '__main__':
    input_sequence = [
        {'lexeme': 'const', 'token_type': 'IDE', 'number_line': 1},
        {'lexeme': '{', 'token_type': 'DEL', 'number_line': 1},
        {'lexeme': 'int', 'token_type': 'IDE', 'number_line': 2},
        {'lexeme': 'a', 'token_type': 'IDE', 'number_line': 2},
        {'lexeme': '=', 'token_type': 'REL', 'number_line': 2},
        {'lexeme': '5', 'token_type': 'NRO', 'number_line': 2},
        {'lexeme': ';', 'token_type': 'DEL', 'number_line': 2},
        {'lexeme': '}', 'token_type': 'DEL', 'number_line': 3},
    ]

parser = GoatParser(input_sequence)
result = parser.program()

if result:
    print("Análise sintática concluída com sucesso!")
else:
    print("Erro na análise sintática.")
