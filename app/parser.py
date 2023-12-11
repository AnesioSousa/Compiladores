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
            return self.constant()

    def constant(self):
        if self.type():
            return self.constalt()
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
            return self.valor()
        return True

    def valor(self):
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
    
    