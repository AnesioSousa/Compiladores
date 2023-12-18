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

    def __init__(self, file_name, input_tokens=[]):
        self._file_name = file_name
        self._input_tokens = input_tokens
        self._lookahead = self._input_tokens[0]
        self._token_counter = 0
        self._output = open(f'./files/{file_name}-saida.txt', 'a', encoding='utf-8')
        
    def program(self):
        ans = self.constant_block() and self.variable_block() and self.class_block() and self.object_block() and self.main_class()
        if not ans:
            self.error()
        return ans
   
    def error(self):
        sync_tokens = [';']
        self._output.write(f"Syntax Error: Found: '{self._lookahead['lexeme']}', number_line: {self._lookahead['number_line']}\n") 

        while(self._lookahead['lexeme'] not in sync_tokens):
            self._lookahead = self.next_token()
            if(self._token_counter == len(self._input_tokens)-1):
                break
        self._lookahead = self.next_token()

    def a(self):
        ans = False
        if self._lookahead['lexeme'] == 'variables':
            self.match('variables')
            ans = self.variable_block() and self.c()
            
        return ans
    
    def b(self):
        ans = True
        if self._lookahead['lexeme'] == 'const':
            self.match('const')
            ans = self.constant_block() and self.c()
        
        return ans
        
    def c(self):
        ans = False
        if self._lookahead['lexeme'] == 'objects':
            self.match('objects')
            ans = self.objects()
        elif self._lookahead['lexeme'] == 'class':
            self.match('class')
            if self._lookahead['lexeme'] == 'main':
                self.match('main')
                ans = self.main()
            elif self.class_block():
                ans = self.c()
        return ans
    
    def variable_block(self):
         if self._lookahead['lexeme'] == '{':
            self.match('{')
            self.variable()
            if self._lookahead['lexeme'] == '}':
                self.match('}')

    def variable(self):
        ans=False
        if self.type():
            if self.ide():
                if self.optional_value() and self.variable_same_line():
                    if self._lookahead['lexeme'] == ';':
                        return self.variable()
        elif self.ide():
            if self.for_init():
                if self._lookahead['lexeme'] == ';':
                    self.match(';')
                    ans = True
        
        if ans:
            
            print("Variable read successfully")
        return ans
    
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
            self._output.write(f"Syntax Error: The for statement initialization needs to be an integer! Found: '{self._lookahead['lexeme']}', number_line: {self._lookahead['number_line']}\n")
            self.error()

        return False
    
    def variable_same_line(self):
        if self._lookahead['lexeme'] == ',':
            if self.ide():
                return self.optional_value() and self.variable_same_line()

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
        elif self.array():
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
        if (self._token_counter < len(self._input_tokens)-1):
            self._token_counter += 1
        return self._input_tokens[self._token_counter]

    def constant_block(self):
        if self._lookahead['lexeme'] == 'const':
            self.match('const')
            if self._lookahead['lexeme'] == '{':
                self.match('{')
                if self.constant():
                    if self._lookahead['lexeme'] == '}':
                        self.match('}')
                else:
                    return False
        print('Const read sucessfully')
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
            if self.object_value():
                return True
            elif self.access_expression():
                return True
        elif self.value():
            return True
        elif self.array():
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
        if self._lookahead['lexeme'] in ['int','string', 'boolean', 'real']:
            self.A()
            if self._lookahead['lexeme'] in ['[']:
                return self.B()
            
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
        else:
            return False  # ERRO
        
    def B(self):
        if self._lookahead['lexeme'] in ['[']:
            return self.array()
                
        return False  # ERRO

    def array(self):
        if self._lookahead['lexeme'] == '[':
            self.match('[')
            if self.array_value() and self.more_array_value():
                if self._lookahead['lexeme'] == ']':
                    self.match(']')
                    return True
            return True
            
        return False
   
    def more_array_value(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            if self.array_value() and self.more_array_value():
                    return True
        return True
    
    def array_value(self):
        if self.possible_value():
            if self._lookahead['lexeme'] == ']':
                self.match(']')
                return True
        elif self.array():
            return True

        return False

    def object_value(self):
        if self._lookahead['lexeme'] == '.':
            self.match('.')
            return self.ide()

        return True

    def value(self):
        if self._lookahead['token_type'] == 'NRO':
            return self.number()
        elif self._lookahead['token_type'] == 'CAC':
            return self.match(self._lookahead['lexeme'])
        elif self._lookahead['token_type'] == 'IDE':
            return self.ide()
        #Rever isso!
        elif self._lookahead['lexeme'] in ['true', 'false']:
            return self.bool()
        return False

    def number(self):
        if self._lookahead['token_type'] == 'NRO':
            self.match(self._lookahead['lexeme'])
            return True

        return False

    def possible_value(self):
        if self.ide():
            return self.object_value()
        elif self.value():
            return True

        return True
    
    def main_class(self):
        if self._lookahead['lexeme'] == 'class':
            self.match('class')
            if self._lookahead['lexeme'] == 'main':
                self.match('main')
                if self._lookahead['lexeme'] == '{':
                    self.match('{')
                    ans = self.main_class_content()
                    if self._lookahead['lexeme'] == '}':
                        self.match('}')
                        return ans
        
        return False
    
    def main_class_content(self):
        return self.variable_block() and self.object_block() and self.statement_sequence()
    
    
    def object_block(self):
        if self._lookahead['lexeme'] == 'objects':
            self.match('objects')
            if self._lookahead['lexeme'] == '{':
                self.match('{')
                self.object()
                if self._lookahead['lexeme'] == '}':
                    self.match('}')
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
        if self.statement() and self.statement_sequence():
            pass
        elif self.command() and self.statement_sequence():
            pass
        elif self.expression_sequence() and self.statement_sequence():
            pass
        
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
                        self.statement_sequence()
                        if self._lookahead['lexeme'] == '}':
                            self.match('}')
                            self.else_statement()
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
        if self.logical_and_expression():
            return True
        elif self.logical_or_expression():
            return True
        elif self._lookahead['lexeme'] == '(':
            self.match('(')
            if self.logical_and_expression():
                if self._lookahead['lexeme'] == ')':
                    self.match(')')
                    return True
        elif self._lookahead['lexeme'] == 'this':
            self.match('this')
            if self._lookahead['lexeme'] == '.':
                self.match('.')
                if self.ide():
                    return True
        elif self._lookahead['token_type'] == 'IDE':
            return self.assignment_value()
                
                
        return False
    
    def logical_or_expression(self):
        if self.logical_not_expression():
            pass
        elif self.logical_or_expression():
            if self._lookahead['lexeme'] == '||':
                self.match('||')
                return self.logical_not_expression()
            else:
                return False
        elif self._lookahead['lexeme'] == '(':
            self.match('(')
            if self.logical_or_expression():
                if self._lookahead['lexeme'] == ')':
                    self.match(')')
                    return True
                
        return False
        
        
    def logical_not_expression(self):
        if self.equality_expression():
            pass
        elif self._lookahead['lexeme'] == '!':
            self.match('!')
            return self.logical_not_expression()
        
        return False
    
    def equality_expression(self):
        return self.relational_expression() and self.equality_expression_list()
    
    def equality_expression_list(self):
        if self._lookahead['lexeme'] == '!=':
            self.match('!=')
            return self.relational_expression()
        elif self._lookahead['lexeme'] == '==':
            self.match('==')
            return self.relational_expression()
        
        return True
    
    def relational_expression(self):
        return self.additive_expression() and self.relational_expression_list()
    
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
                if self.variable() and self.logical_and_expression():
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
        return self.access_expression() and self.unary_expression_list()
    
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
        if self.assignment_value() and self.assignment_value_list():
            return True
    
    def assignment_value_list(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            self.args_list()
    
    #Rever isso: Const analisa strings sem precisar disso!
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
        return self.unary_expression() and self.multiplicative_expression_list()
    
    def multiplicative_expression_list(self):
        if self._lookahead['lexeme'] == '*':
            self.match('*')
            return self.unary_expression()
        elif self._lookahead['lexeme'] == '/':
            self.match('/')
            return self.unary_expression()
        
        return True
    def parameter(self):
        if self.type():
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
                    if self.class_content():
                        if self._lookahead['lexeme'] == '}':
                            self.match('}')
                            self.class_block()
            else:
                return False
                        
    def class_extends(self):
        if self._lookahead['lexeme'] == 'extends':
            self.match('extends')
            if not self.ide():
                return False
            
        return True
    
    def class_content(self):
        return self.variable_block() and self.constructor() and self.methods()
        
        
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
        if self.ide():
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
                if self.possible_value():
                    if self._lookahead['lexeme'] == ')':
                        self.match(')')
                        if self._lookahead['lexeme'] == ';':
                            self.match(';')
                            return True
                        
        return False
    
    def read_command(self):
        if self._lookahead['lexeme'] == 'read':
            self.match('read')
            if self._lookahead['lexeme'] == '(':
                self.match('(')
                if self.ide():
                    if self.object_value():
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
                                            self.method()
        elif self._lookahead['lexeme'] == 'void':
            if self.ide():
                if self._lookahead['lexeme'] == '(':
                    self.match('(')
                    self.parameter()
                    if self._lookahead['lexeme'] == ')':
                        self.match(')')
                        if self._lookahead['lexeme'] == '{':
                            self.match('{')
                            self.statement_sequence()
                            if self._lookahead['lexeme'] == '}':
                                self.match('}')
                                self.method()