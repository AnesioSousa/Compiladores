"""
Universidade Estadual de Feira de Santana
EXA869 - MI - PROCESSADORES DE LINGUAGEM DE PROGRAMAÇÃO - TP02 - 2023.2
Autor: Anésio Neto 
Docente: Matheus Pires


const { 
    int MAX = 10, MIN = 0;
    real soma = 33.85;
    string[50] msg = "TESTE", msg2 = "oi";
    int number = objeto.idade;
    real[50] valor = objeto.valor, juros = 27.5;
}

"""


class GoatParser:
    """
    Classe que possibilita a criação de objetos
    capazes de gerar árvores sintáticas partindo de tokens de entrada.
    """

    def __init__(self, input_tokens=[]):
        self._input_tokens = input_tokens
        self._lookahead = self._input_tokens[0]
        self._token_counter = 0
        self.symbol_table = []
        self.last_type = None
        
    def declarations(self):
        ans = True
        if self._lookahead['lexeme'] == 'const':
            self.match('const')
            ans = self.constant_block() and self.a()
        elif self._lookahead['lexeme'] == 'variables':
            self.match('variables')
            ans = self.variable() and self.b()
        return ans

    def a(self):
        ans = False
        if self._lookahead['lexeme'] == 'variables':
            self.match('variables')
            if self._lookahead['lexeme'] == '{':
                self.match('{')
                ans = self.variable() and self.c()
            
        return ans
    # pode haver código sem const-block!
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
    
    
    def variable(self):
        ans=False
        if self.type():
            self.varinitcontmatr()
            if self.ide():
                ans = self.varcont()
        return ans
    
    def varcont(self):
        return self.varinit() and self.varfinal()
    
    def varinit(self):
        if self._lookahead['lexeme'] in [',',';']:
            return True
        if self._lookahead['lexeme'] == '=':
            self.match('=')
            return self.value()
        if self._lookahead['lexeme'] == '.':
            self.match('.')
            return self.varinit()
        elif self._lookahead['token_type'] == 'IDE':
                if self.ide():
                    return self.varfinal()
        #vetores
        elif self._lookahead['lexeme'] == '[':
            self.match('[')
            ans = False
            if self._lookahead['token_type'] == 'NRO':
                ans = self.number()
            elif self._lookahead['token_type'] == 'IDE':
                ans = self.ide()
            if ans and self.match(']'):
                return self.varinitcont()
        return False
    
    def varinitcont(self): 
        if self._lookahead['lexeme'] in [';',',']:
            return True 
        if self._lookahead['lexeme'] == '=':
            self.match('=')
            if self.match('{'):
                return self.vetor()
        elif self._lookahead['lexeme'] == '[':
            self.match('[')
            ans = False
            if self._lookahead['token_type'] == 'NRO':
                ans = self.number()
            elif self._lookahead['token_type'] == 'IDE':
                ans = self.ide()
            if ans and self.match(']'):
                return self.varinitcontmatr()
        return False
    
    def varinitcontmatr(self):
        if self._lookahead['lexeme'] == ';':
            return True  
        elif self._lookahead['lexeme'] == '{':
            self.match('{')
            if self.vetor():
                if self.match(',') and self.match('{'):
                    return self.vetor()
        elif self._lookahead['lexeme'] == '[':
            self.match('[')
            ans = False
            if self._lookahead['token_type'] == 'NRO':
                ans = self.number()
            elif self._lookahead['token_type'] == 'IDE':
                ans = self.ide()
            if ans and self.match(']'):
                if self._lookahead['lexeme'] == '=':
                    self.match('=')
                    ans = self.match('{')
                    if ans and self.vetor():
                        if self.match(',') and self.match('{'):
                            if self.vetor():
                                if self.match(',') and self.match('{'):
                                    return self.vetor()
                elif self._lookahead['lexeme'] == ';':
                    return True
        return False
    
    def vetor(self):
        if self.value():
            return self.vetorcont()
        return False

    def vetorcont(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            return self.vetor()
        elif self._lookahead['lexeme'] == '}':
            self.match('}')
            return True
        return False
    
    def varfinal(self):
        if self._lookahead['lexeme'] == ',':
            self.match(',')
            return self.varalt()
        elif self._lookahead['lexeme'] == ';':
            self.match(';')
            return self.varfim()
        elif self._lookahead['lexeme'] == '.':
            self.match('.')
            return self.varinit()
        return False
    
    def varalt(self):
        if self.ide():
            return self.varcont()        
        return False
    
    def varfim(self):
        if self._lookahead['lexeme'] == '}':
            return self.match('}')
        return self.variable()

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
            if self.number():
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
        # fazer CAC
        return False

        #fazer CAC
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
            return self.number()
        elif self._lookahead['token_type'] == 'CAC':
            return self.match(self._lookahead['lexeme'])
        elif self._lookahead['token_type'] == 'CAC':
            return self.match(self._lookahead['lexeme'])
        elif self._lookahead['token_type'] == 'IDE':
            return self.ide()
        return False

    def follow(self, k=1):
        return self._input_tokens[self.i+k]

    def number(self):
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
