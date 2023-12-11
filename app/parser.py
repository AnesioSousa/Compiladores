"""
Universidade Estadual de Feira de Santana
EXA869 - MI - PROCESSADORES DE LINGUAGEM DE PROGRAMAÇÃO - TP02 - 2023.2
Autor: Anésio Neto 
Docente: Matheus Pires
"""
# Tem que fazer uma função (ou método) para cada não terminal. Desde <program> até <boolean>.

# from lexer import LexicalAnalyser

tokens = [
    {
        "line": "01",
        "type": "IDE",
        "lexeme": "exemplo"
    },
    {
        "line": "01",
        "type": "DEL",
        "lexeme": ";"
    },
]


class GoatParser:
    """
    Classe que possibilita a criação de objetos
    capazes de gerar árvores sintáticas partindo de tokens de entrada.
    """

    def __init__(self, input_tokens=[], pathof_output_file=None):
        self._input_tokens = input_tokens
        self._output_file = pathof_output_file
        self._lookahead = self._input_tokens[0]
        #print(self._lookahead)
        self._char_counter = 0
        self.symbol_table = []
        self.last_type = None
    
    def run(self):
        ans = True
        if self._lookahead['lexeme'] == 'const':
            self.match('const')
            ans = self.constant_block()  # and self.b()
        return ans

    def match(self, symbol):
        if symbol == self._lookahead['lexeme']:
            self._lookahead = self.le_token()
            return True
        else:
            # print(f"expected {symbol}, found {self.lookahead['lexeme']}\n")
            return False

    def le_token(self):
        if (self._char_counter < len(self._input_tokens)-1):
            self._char_counter += 1
        return self._input_tokens[self._char_counter]

    def constant_block(self):
        if self._lookahead['lexeme'] == '{':
            self.match('{')
            if self.constant():
                if self._lookahead['lexeme'] == '}':
                    self.match('}')
            else:
                return False
        return True

    def constant(self):
        if self.type():
            return self.constant_alt()
        # Pode ser vazio
        return True

    
    def constant_alt(self):
        if self.constant_alt_mtrz() and self.ide():
            if self._lookahead['lexeme'] == '=':
                self.match('=')
                if self.assignment_value() and self.constant_same_line():
                    if self._lookahead['lexeme'] == ';':
                        self.match(';')
                        return self.constant()  
                else:
                    return False
        else:
                return False
            
        
    def constant_alt_mtrz(self):
        if self._lookahead['lexeme'] == '[':
            self.match('[')
            if self.nro():
                if self._lookahead['lexeme'] == ']':
                    self.match(']')
                    return True
            else:
                return False
        
        # pode ser vazio
        return True
                
            
                
        
        
    def assignment_value(self):
        if self.ide():
            return self.object_value()
        elif self.value():
            return True
        elif self.array():
            return True
        #fazer CAC
        return False
    
    def value(self):
        if self._lookahead['token_type'] == 'NRO':
            return self.nro()
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
        #Rever isso aqui!
        return False
    
    def constalt(self):
        if self.ide():
            if self.varinit():
                return self.constcont()
        return False
    
    def constcont(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            return self.constalt()
        elif self._lookahead['lexeme'] == ';':
            self.match(';')
            return self.constfim()
        return False

    def constfim(self):
        if self._lookahead['lexeme'] == '}':
            return self.match('}')
        return self.constant() # Strange

    def ide(self):
        if self._lookahead['token_type'] == 'IDE':
            self.last_ide = self._lookahead['lexeme']
            self.match(self._lookahead['lexeme'])
            return True
        return False

    def type(self):
        if self._lookahead['lexeme'] == 'int':
            # LETOKEN
            self.last_type = 'int'
            self.match('int')
        elif self._lookahead['lexeme'] == 'string':
            self.last_type = 'string'
            self.match('string')
        elif self._lookahead['lexeme'] == 'boolean':
            self.last_type = 'boolean'
            self.match('boolean')
        elif self._lookahead['lexeme'] == 'real':
            self.last_type = 'real'
            self.match('real')
        else:
            return False  # ERRO

        return True
    
    def varinit(self):
        if self._lookahead['lexeme'] == '=':
            self.match('=')
            return self.value()
        return True
    

    
    def array(self):
        if self._lookahead['lexeme'] == '[':
            self.match('[')
            return self.array_value() and self.more_array_value()
        
    def array_value(self):
        if self.possible_value():
            pass
        elif self.array():
            pass
        
        return False

    def object_value(self):
        if self._lookahead['lexeme'] == '.':
            self.match('.')
            return self.ide()
        
        return True
        
    def value(self):
        if self._lookahead['token_type'] == 'NRO':
            return self.nro()
        return False
    
    def follow(self, k=1):
        return self._input_tokens[self.i+k]
    
    def nro(self):
        if self._lookahead['token_type'] == 'NRO':
            self.match(self._lookahead['lexeme'])
            return True
        
        return False
    
    def possible_value(self):
        if self._lookahead['token_type'] == 'IDE':
            self.match(self.lookahead['lexeme'])
            return self.object_value()
        elif self.value():
            return True
        
        return True