import json

class SintaxAnalyzer:
    def __init__(self, input,output_file):
        self.input = input 
        self.lookahead = input[0]
        self.i = 0
        self.symbol_table = []
        self.current_scope = "GLOBAL"
        self.last_ide = None
        self.last_type = None
        self.last_number = {
            "number": None,
            "type": None
        }
        self.function_parameters = []
        # expected symbol for type comparison
        self.expected = None
        self.tag_retorno = {'status':False, 'type':'vazio'}
        self.output = open(output_file, 'a', encoding='utf-8')
        self.semanticStatus = True
        with open('msg_semanticError.json', 'r', encoding='utf-8') as f:
            self.msg_error = json.load(f)

    def run(self):
        ans = self.start()
        print(self.symbol_table)
        return ans and self.semanticStatus

    def match(self, t):
        if t == self.lookahead['lexeme']:
            self.lookahead = self.next_terminal()
            return True
        else:
            # print(f"expected {t}, found {self.lookahead['lexeme']}\n")
            return False

    def next_terminal(self):
        if(self.i < len(self.input)-1): self.i = self.i+1
        return self.input[self.i]

    def follow(self, k=1):
        return self.input[self.i+k]

    def save_symbol(self, category):
        symbol = { 
            "lexeme": self.last_ide, 
            "category": category,
            "type": self.last_type,
            "scope": self.current_scope,
            "parameters": self.function_parameters
        }
        id = 1
        for symb in self.symbol_table:
            if symbol['category'] == 'FUNCAO' and symbol['lexeme'] == symb['lexeme']:
                if symbol['parameters'] != symb['parameters']:
                    id = id + 1
                else: 
                    print("not saved: ", symbol, symb)
                    self.semanticError(symb)
                    return
            elif symbol['lexeme'] == symb['lexeme']:
                self.semanticError(symb)
                return
        if symbol['category'] == 'FUNCAO': symbol['scope'] = self.current_scope = symbol['scope']+f" {id}"
        self.symbol_table.append(symbol)

    def remove_symbol(self, scope ):
        for symbol in self.symbol_table:
            if symbol['scope'] == scope and symbol['category'] != 'FUNCAO':
                self.symbol_table.remove(symbol)

    def get_symbol(self, lexeme: str) -> dict:
        for symbol in self.symbol_table:
            if symbol['lexeme'] == lexeme:
                return symbol
            elif symbol['category'] == 'FUNCAO':
                for param in symbol['parameters']:
                    if param['lexeme'] == lexeme:
                        return {'lexeme':param['lexeme'],'category':'VAR','type':param['type'],'scope':symbol['scope']}
        return None

    def get_functions(self, lexeme: str) -> list:
        symbols = []
        for symbol in self.symbol_table:
            if symbol['lexeme'] == lexeme and symbol['category'] == 'FUNCAO':
                symbols.append(symbol)
        return symbols

    def get_symbol_by_scope(self, scope: str) -> dict:
        """
        Returns the symbol of the function with given scope.
        Note: the scope is unique
        """
        for symbol in self.symbol_table:
            if symbol['scope'] == scope and symbol['category'] == 'FUNCAO':
                return symbol
        return None

    def is_integer(self, number: str) -> bool:
        x = self.lookahead['lexeme'].find(".")
        if(x >= 0):
            return False
        return True

    def error(self):
        sync_tokens = [';']
        self.output.write(f"Syntax Error: Found: '{self.lookahead['lexeme']}', line: {self.lookahead['line']}\n") 

        while(self.lookahead['lexeme'] not in sync_tokens):
            self.lookahead = self.next_terminal()
            if(self.i == len(self.input)-1):
                break
        self.lookahead = self.next_terminal()

    def semanticError(self, symbol=None, type=1):
        if symbol:
            self.output.write(f"Semantic Error:  {symbol['category']} '{symbol['lexeme']}' " + self.msg_error[type-1] + f" - line: {self.lookahead['line']}\n") 
        else:
            self.output.write(f"Semantic Error:  " + self.msg_error[type-1] + f" - line: {self.lookahead['line']}\n") 
        self.semanticStatus = False

    def attributionTypeError(self, symbol: dict, receivedType: str = None) -> None:
        if(symbol["type"] == "inteiro"):
            self.semanticError(symbol, 3)
        elif(symbol["type"] == "real"):
            self.semanticError(symbol, 5)
        elif(symbol["type"] == "cadeia"):
            self.semanticError(symbol, 6)
        elif(symbol["type"] == "char"):
            self.semanticError(symbol, 7)
        elif(symbol["type"] == "booleano"):
            self.semanticError(symbol, 8)

    def check_parameter(self, symbol: dict, receivedType: str = None):
        if symbol:
            if symbol["paran_current"] >= len(symbol["parameters"]):
                self.semanticError(symbol, 17)
            else:
                if ((type == "real" and receivedType not in ["inteiro", "real"]) or
                    (type != "real" and type != receivedType)):
                    self.semanticError(symbol, 16)
            symbol["paran_current"] += 1

    def start(self):
        ans = False
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            ans = self.algoritmo()
        elif self.lookahead['lexeme'] == 'funcao':
            self.match('funcao')
            if self.funcao():
                ans = self.start()
        elif self.lookahead['lexeme'] == 'variaveis':
            self.match('variaveis')
            ans = self.variaveis() and self.a()
        elif self.lookahead['lexeme'] == 'constantes':
            self.match('constantes')
            ans = self.constantes() and self.b()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            ans = self.registro() and self.start()            
        if not ans:
            self.error()
        return ans

    def a(self):
        ans = False
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            ans = self.algoritmo()
        elif self.lookahead['lexeme'] == 'funcao':
            self.match('funcao')
            if self.funcao():
                ans = self.a()
        elif self.lookahead['lexeme'] == 'constantes':
            self.match('constantes')
            ans = self.constantes() and self.c()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            ans = self.registro() and self.a()
        return ans

    def b(self):
        ans = False
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            ans = self.algoritmo()
        elif self.lookahead['lexeme'] == 'funcao':
            self.match('funcao')
            if self.funcao():
                ans = self.b()
        elif self.lookahead['lexeme'] == 'variaveis':
            self.match('variaveis')
            ans = self.variaveis() and self.c()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            ans = self.registro() and self.b()
        return ans

    def c(self):
        ans = False
        if self.lookahead['lexeme'] == 'algoritmo':
            self.match('algoritmo')
            ans = self.algoritmo()
        elif self.lookahead['lexeme'] == 'funcao':
            self.match('funcao')
            if self.funcao():
                ans = self.c()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            ans = self.registro() and self.c()
        return ans

    def algoritmo(self):
        self.current_scope = "ALGORITMO"
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            ans=True
            while(self.lookahead['lexeme'] != '}' and self.i < len(self.input)-1):
                result = self.conteudo()
                if not result:
                    self.error()
                    ans = result
            return ans and self.match('}')
        return False

    def conteudo(self):
        if self.lookahead['lexeme'] == 'variaveis':
            self.match('variaveis')
            return self.variaveis()
        elif self.lookahead['lexeme'] == 'constantes':
            self.match('constantes')
            return self.constantes()
        elif self.lookahead['lexeme'] == 'se':
            self.match('se')
            return self.se()
        elif self.lookahead['lexeme'] == 'enquanto':
            self.match('enquanto')
            return self.enquanto()
        elif self.lookahead['lexeme'] == 'escreva':
            self.match('escreva')
            return self.escreva()
        elif self.lookahead['lexeme'] == 'leia':
            self.match('leia')
            return self.leia()
        elif self.lookahead['lexeme'] == 'para':
            self.match('para')
            return self.para()
        elif self.lookahead['lexeme'] == 'registro':
            self.match('registro')
            return self.registro()
        elif self.lookahead['lexeme'] == 'retorno':
            self.match('retorno')
            return self.retorno()
        elif self.lookahead['type'] == 'IDE':
            ide = self.lookahead['lexeme']
            symbol = self.get_symbol(ide)
            if symbol != None and symbol['category'] == "CONST":
                self.semanticError(symbol, type=9)
            if self.acessovar():
                if self.lookahead['lexeme'] == '=':
                    self.match('=')
                    if self.expatribuicao(symbol):
                        return self.match(';')
                elif self.lookahead['lexeme'] == '(':
                    if self.chamadafuncao(symbol):
                        return self.match(';')
        return False

    def escreva(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.escont()
        return False

    def escont(self):
        if self.acessovar() or self.cadeia() or self.char():
            return self.esfim()
        return False

    def esfim(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.escont()
        elif self.lookahead['lexeme'] == ')':
            self.match(')')
            self.match(';')
            return True
        return False

    def leia(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.leiacont()
        return False

    def leiacont(self):
        if self.acessovar():
            return self.leiafim()
        return False

    def leiafim(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.leiacont()
        elif self.lookahead['lexeme'] == ')':
            self.match(')')
            return self.match(';')
        return False
            
    def acessovar(self, expected=None):
        if self.lookahead['type'] == 'IDE':
            symbol = self.get_symbol(self.lookahead['lexeme'])
            if symbol == None:
                self.semanticError({'lexeme':self.lookahead['lexeme'], 'category':'VAR'}, type=4)
            elif expected != None and symbol['type'] != expected['type']:
                if self.tag_retorno['status']:
                    #self.semanticError(symbol, type=14)
                    self.tag_retorno['type'] = symbol['type']
                else: self.semanticError(symbol, type=13)
            return self.ide() and self.acessovarcont()
        return False

    def check_ide_as_integer(self):
        symbol = self.get_symbol(self.last_ide)
        if symbol != None and symbol['type'] != 'inteiro':
            self.semanticError(symbol, type=3)

    def acessovarcont(self):
        if self.lookahead['lexeme'] == '.':
            self.match('.')
            return self.acessovar()
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            token = self.lookahead['lexeme']
            if self.nro(1):
                self.match(']')
                return self.acessovarcontb()
            elif self.ide():
                self.check_ide_as_integer()
                if self.match(']'):
                    return self.acessovarcontb()
            else:
                self.semanticError({'lexeme':token, 'category':'INDEX'}, type=3)
        return True

    def acessovarcontb(self):
        if self.lookahead['lexeme'] in [',', ')','=',';']:
            return True
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.nro(1) and self.match(']'):
                return self.acessovarcontc()
            elif self.ide():
                self.check_ide_as_integer()
                if self.match(']'):
                    return self.acessovarcontc()
            else:
                self.semanticError(type=3)
        return False

    def acessovarcontc(self):
        if self.lookahead['lexeme'] in [',', ')']:
            return True
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.nro(1): 
                return self.match(']')
            elif self.ide():
                self.check_ide_as_integer()
                return self.match(']')
            else:
                self.semanticError(type=3)
        return False

    def follow_condicional(self):
        follow = self.follow()
        i=1
        rel_log = False
        while follow['lexeme'] not in [')','{','}']:
            follow = self.follow(i)      
            if follow['type'] in ['REL','LOG']:
                rel_log=True
                break
            i += 1
            if self.i+i >= len(self.input): break
        return rel_log

    def se(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            rel_log = self.follow_condicional()
            if rel_log:
                if self.expressao():
                    if self.function_cont():
                        return self.senao()
            elif self.lookahead['lexeme'] in ['verdadeiro','falso']:
                self.bool()
                if self.function_cont():
                    return self.senao()
            elif self.lookahead['type'] == 'IDE':
                if self.acessovar():
                    if self.function_cont():
                        return self.senao()
        return False

    def senao(self):
        if self.lookahead['lexeme'] == 'senao':
            self.match('senao')
            if self.match('{'):
                if self.conteudo():
                    return self.match('}')
        return True

    def exparitmetica(self, symbol=None):
        operation = {
            "symbol": symbol,
            "parts": []
        }
        if self.lookahead['lexeme'] in ['++','--']:
            self.expatribuicaocont()
            if self.acessovar():
                return self.exparitmeticacont(operation)
        if self.nro():
            operation["parts"].append(self.last_number.copy())
            return self.exparitmeticacont(operation)
        elif self.acessovar():
            part = self.get_symbol(self.last_ide)
            operation["parts"].append(part)
            self.expatribuicaocont()
            return self.exparitmeticacont(operation)
        elif self.lookahead['lexeme'] == '-':
            self.match('-')
            if self.negativo():
                return self.exparitmeticacont(operation)
        elif self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.exparitmeticaparen(operation)
        return False

    def exparitmeticaparen(self, operation):
        if self.exparitmetica():
            if self.match(')'):
                return self.exparitmeticacontb(operation)
        return False

    def exparitmeticacont(self, operation=None):
        if self.lookahead['type'] == 'ART':
            if self.lookahead['lexeme'] == '/':
                type = 1
            else:
                type = 0
            self.match(self.lookahead['lexeme'])
            return self.exparitmeticab(type, operation)
        return False

    def exparitmeticab(self, type=0, operation=None):
        if type == 1 and self.lookahead['lexeme'] == '0':
            self.semanticError(type=10)
        if self.acessovar():
            part = self.get_symbol(self.last_ide)
            operation["parts"].append(part)
            return self.exparitmeticacontb(operation)
        elif self.nro():
            operation["parts"].append(self.last_number.copy())
            return self.exparitmeticacontb(operation)
        elif self.lookahead['lexeme'] == '-':
            self.match('-')
            if self.negativo():
                return self.exparitmeticacontb(operation)
        elif self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.exparitmeticabparen(operation)
        return False

    def exparitmeticabparen(self, operation):
        if self.exparitmetica():
            if self.match(')'):
                return self.exparitmeticacontb(operation)
        return False

    def exparitmeticacontb(self, operation=None):
        if self.lookahead['type'] == 'ART':
            if self.lookahead['lexeme'] == '/':
                type = 1
            else:
                type = 0
            self.match(self.lookahead['lexeme'])
            return self.exparitmeticab(type, operation)

        if operation:
            symbol = operation["symbol"]
            invalid_type = False
            is_inteiro = True

            for i in operation["parts"]:
                if i == None: continue
                if i["type"] != 'inteiro':
                    is_inteiro = False
                if i["type"] not in ['inteiro', 'real']:
                    invalid_type = True
            
            if invalid_type:
                self.semanticError(symbol, 11)
            
            if symbol:
                if symbol["category"] == "FUNCAO" and "paran_current" in symbol.keys():
                    if is_inteiro:
                        type = "inteiro"
                    else:
                        type = "real"
                    self.check_parameter(symbol, type)
                    # if not is_inteiro and symbol["parameters"][symbol["paran_current"]]["type"] == 'inteiro':
                    #     self.parameterTypeError(symbol, "real")
                else:
                    if not is_inteiro and symbol["type"] == 'inteiro':
                        self.semanticError(symbol, 12)
            
            if self.tag_retorno['status']: 
                self.tag_retorno['type'] = ( 'inteiro' if is_inteiro else 'real' )
        return True

    def expatribuicao(self, symbol=None):
        if symbol is None: 
            symbol = self.get_symbol(self.last_ide)

        if(symbol is None):
            typeOperation = 0
        else:
            typeOperation = 1
        if self.lookahead['lexeme'] in ['++','--']:
            self.match(self.lookahead['lexeme'])
            if self.lookahead['type'] == 'NRO':
                return self.nro()
            elif self.lookahead['type'] == 'IDE':
                return self.acessovar()
        elif self.lookahead['type'] in ['IDE', 'NRO']:
            follow = self.follow()
            if follow['lexeme'] in ['++','--']:
                self.match(self.lookahead['lexeme'])
                return self.expatribuicaocont() 
            elif self.valor(typeOperation, symbol):
                return self.expatribuicaocont() 
            return False
        return self.valor(typeOperation, symbol)
        
    def expatribuicaocont(self):
        if self.lookahead['lexeme'] in ['++','--']:
            self.match(self.lookahead['lexeme'])
        return True
        
    def cadeia(self):
        if self.lookahead['type'] == 'CAD':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def char(self):
        if self.lookahead['type'] == 'CAR':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def ide(self):
        if self.lookahead['type'] == 'IDE':
            self.last_ide = self.lookahead['lexeme']
            self.match(self.lookahead['lexeme'])
            return True
        return False
    
    def nro(self, type=0, symbol=None):
        """
        Function for check a number

        Parameters:
            type (int): 1 if the number must be an integer, 0 otherwise
            symbol (dict): symbol in symbol table

        Returns:
            bool: Returning if code syntax code its valid
        """
        if self.lookahead['type'] == 'NRO':
            self.last_number["number"] = self.lookahead['lexeme']
            if self.lookahead['lexeme'].find('.') >= 0:
                self.last_number["type"] = "real"
                if type == 1:
                    if symbol is None: symbol = {'lexeme':self.lookahead['lexeme'], 'category':'INDEX'}
                    self.semanticError(symbol, type=3)
                if type == 2:
                    self.check_parameter(symbol, "real")
                    # if symbol is None or symbol["parameters"][symbol["paran_current"]]["type"] == "inteiro":
                    #     self.parameterTypeError(symbol, "real")
            else:
                if type == 2:
                    self.check_parameter(symbol, "inteiro")
                self.last_number["type"] = "inteiro"


            self.match(self.lookahead['lexeme'])
            return True
        return False

    def simbolo(self):
        if self.lookahead['type'] == 'SIB':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def negativo(self):
        if self.lookahead['type'] == 'NRO':
            return self.nro()
        if self.lookahead['type'] == 'IDE':
            return self.acessovar()
        return False

    def constantes(self):
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            return self.const()
        return False

    def const(self):
        if self.tipo():
            return self.constalt()
        return False

    def tipo(self):
        if self.lookahead['lexeme'] == 'inteiro':
            self.last_type = 'inteiro'
            self.match('inteiro')
        elif self.lookahead['lexeme'] == 'real':
            self.last_type = 'real'
            self.match('real')
        elif self.lookahead['lexeme'] == 'booleano':
            self.last_type = 'booleano'
            self.match('booleano')
        elif self.lookahead['lexeme'] == 'cadeia':
            self.last_type = 'cadeia'
            self.match('cadeia')
        elif self.lookahead['lexeme'] == 'char':
            self.last_type = 'char'
            self.match('char')
        elif self.lookahead['lexeme'] == 'registro':
            self.last_type = 'registro'
            self.match('registro')
        else:
            return False
        return True

    def constalt(self):
        if self.ide():
            self.save_symbol("CONST")
            if self.varinit():
                return self.constcont()
        return False

    def varinit(self):
        symbol = self.get_symbol(self.last_ide)
        self.expected = symbol
        typeOperation = ( 0 if symbol is None else 1 )
        if self.lookahead['lexeme'] in [',',';']:
            return True
        if self.lookahead['lexeme'] == '=':
            self.match('=')
            return self.valor(typeOperation, symbol)
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            ans = False
            if self.lookahead['type'] == 'NRO':
                ans = self.nro(1)
            elif self.lookahead['type'] == 'IDE':
                ans = self.ide()
                self.check_ide_as_integer()
            if ans and self.match(']'):
                return self.varinitcont()
        return False

    def varinitcont(self): 
        if self.lookahead['lexeme'] in [';',',']:
            return True 
        if self.lookahead['lexeme'] == '=':
            self.match('=')
            if self.match('{'):
                return self.vetor()
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            ans = False
            if self.lookahead['type'] == 'NRO':
                ans = self.nro(1)
            elif self.lookahead['type'] == 'IDE':
                ans = self.ide()
                self.check_ide_as_integer()
            if ans and self.match(']'):
                return self.varinitcontmatr()
        return False

    def varinitcontmatr(self):
        if self.lookahead['lexeme'] == ';':
            return True  
        elif self.lookahead['lexeme'] == '{':
            self.match('{')
            if self.vetor():
                if self.match(',') and self.match('{'):
                    return self.vetor()
        elif self.lookahead['lexeme'] == '[':
            self.match('[')
            ans = False
            if self.lookahead['type'] == 'NRO':
                ans = self.nro(1)
            elif self.lookahead['type'] == 'IDE':
                ans = self.ide()
                self.check_ide_as_integer()
            if ans and self.match(']'):
                if self.lookahead['lexeme'] == '=':
                    self.match('=')
                    ans = self.match('{')
                    if ans and self.vetor():
                        if self.match(',') and self.match('{'):
                            if self.vetor():
                                if self.match(',') and self.match('{'):
                                    return self.vetor()
                elif self.lookahead['lexeme'] == ';':
                    return True
        return False
            
    def vetor(self):
        symbol = self.expected
        typeOperation = ( 0 if symbol is None else 1 )
        if self.valor(typeOperation, symbol):
            return self.vetorcont()
        return False

    def vetorcont(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.vetor()
        elif self.lookahead['lexeme'] == '}':
            self.match('}')
            return True
        return False

    def constcont(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.constalt()
        elif self.lookahead['lexeme'] == ';':
            self.match(';')
            return self.constfim()
        return False

    def constfim(self):
        if self.lookahead['lexeme'] == '}':
            return self.match('}')
        return self.const()

    def valor(self, type: int = None, symbol: dict = None) -> bool:
        """
        Function for check a value

        Parameters:
            type (int): Type of operation
                * 0 -> attribution of undeclared variable
                * 1 -> attribution
                * 2 -> function parameter
            symbol (dict): Symbol under validation (used for attribution)

        Returns:
            bool: Returning if code syntax code its valid
        """
        if self.lookahead['lexeme'] == '-':
            follow = self.follow(2)
            if follow['type'] in ['REL', 'LOG']:
                return self.expressao()
            elif follow['type'] == 'ART':
                return self.exparitmetica()
            else:
                self.match('-')
                return self.negativo()
        elif self.lookahead['lexeme'] == '(':
            follow = self.follow()       
            i=2
            rel_log = art = False
            while follow['lexeme'] not in [';','}']:
                follow = self.follow(i)      
                if follow['type'] in ['REL','LOG']:
                    rel_log=True
                elif follow['type'] == 'ART':
                    art=True 
                i += 1
            if rel_log:
                return self.expressao()
            elif art:
                return self.exparitmetica()
        elif self.lookahead['type'] == 'CAD':
            if(type == 1):
                if(symbol is None or symbol["type"] != "cadeia"):
                    self.attributionTypeError(symbol, "cadeia")
            elif(type == 2):
                self.check_parameter(symbol, "cadeia")
                # if(symbol is None or symbol["parameters"][symbol["paran_current"]]["type"] != "cadeia"):
                #     self.parameterTypeError(symbol, "cadeia")
                # symbol["paran_current"] += 1
            return self.match(self.lookahead['lexeme'])
        elif self.lookahead['type'] == 'CAR':
            if(type == 1):
                if(symbol is None or symbol["type"] != "char"):
                    self.attributionTypeError(symbol, "char")
            elif(type == 2):
                self.check_parameter(symbol, "char")
                # if(symbol is None or symbol["parameters"][symbol["paran_current"]]["type"] != "char"):
                #     self.parameterTypeError(symbol, "char")
                # symbol["paran_current"] += 1
            return self.match(self.lookahead['lexeme'])
        elif self.lookahead['type'] == 'NRO':
            follow = self.follow()
            if follow['type'] in ['REL', 'LOG']:
                return self.expressao()
            elif follow['type'] == 'ART':
                return self.exparitmetica(symbol)
            elif type==1 and symbol['type'] == 'inteiro':
                return self.nro(1, symbol)
            elif(type == 2):
                result = self.nro(2, symbol)
                # symbol["paran_current"] += 1
                return result
            else: 
                return self.nro()
        elif self.lookahead['lexeme'] in ['verdadeiro','falso']:
            if(type == 1):
                if(symbol is None or symbol["type"] != "booleano"):
                    self.attributionTypeError(symbol, "booleano")
            elif(type == 2):
                self.check_parameter(symbol, "booleano")
                # if(symbol is None or symbol["parameters"][symbol["paran_current"]]["type"] != "booleano"):
                #     self.parameterTypeError(symbol, "booleano")
                # symbol["paran_current"] += 1
            follow = self.follow()
            if follow['type'] in ['REL', 'LOG']:
                return self.expressao()
            else:
                return self.bool()
        elif self.lookahead['type'] == 'IDE':
            follow = self.follow()
            if follow['type'] in ['REL', 'LOG']:
                return self.expressao()
            elif follow['type'] == 'ART':
                return self.exparitmetica(symbol)
            elif follow['lexeme'] == '(':
                symbols = self.get_functions(self.lookahead['lexeme'])
                self.ide()
                symb = None

                # if function (symb) is not declared
                if len(symbols) > 0:
                    ans = 0
                    i = self.i+1
                    token = self.input[i]
                    while token['lexeme'] != ')':
                        if token['lexeme'] == ',':
                            ans = ans + 1
                        i = i+1
                        token = self.input[i]
                    #takes only the number of parameters, excluding delimiters
                    ans = ans+1
                    find = False
                    for symb in symbols:
                        print(ans, len(symb['parameters']))
                        if len(symb['parameters']) == ans:
                            find = True
                            break
                    print('symb find: ', symb)
                    if symb is None or not find:
                        self.semanticError({'lexeme':self.last_ide, 'category':'FUNCAO'},type=17)
                    # if variable (symbol) has a different type than function return (symb)
                    elif type == 1 and symbol['type'] != symb['type']:
                        self.semanticError(symbol, type=13)
                return self.chamadafuncao(symb)
            else:
                return self.acessovar(symbol)
        return False
            
    def bool(self):
        if self.lookahead['lexeme'] == 'verdadeiro' or self.lookahead['lexeme'] == 'falso':
            self.match(self.lookahead['lexeme'])
            return True
        return False

    def negativo(self):
        return self.nro() or self.acessovar()

    def variaveis(self):
        if self.lookahead['lexeme'] == '{':
            self.match('{')
            return self.var()
        return False
    
    def var(self):
        ans=False
        if self.tipo():
            if self.ide():
                ans = True
                if self.last_type == 'registro':
                    self.last_type = 'registro ' + self.last_ide
                    ans = self.ide()
                self.save_symbol("VAR")
                ans = ans and self.varcont()
        return ans

    def varalt(self):
        if self.ide():
            self.save_symbol("VAR")
            return self.varcont()        
        return False

    def varcont(self):
        return self.varinit() and self.varfinal()

    def varfinal(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.varalt()
        elif self.lookahead['lexeme'] == ';':
            self.match(';')
            return self.varfim()
        return False

    def varfim(self):
        if self.lookahead['lexeme'] == '}':
            return self.match('}')
        return self.var()

    def registro(self):
        if self.lookahead['type'] == 'IDE':
            self.last_ide = self.lookahead['lexeme']
            self.last_type = self.lookahead['type']
            self.ide()
            if self.match('{'):
                self.save_symbol('REGISTRO')
                self.current_scope = self.current_scope + " " + self.last_ide
                if self.lookahead['lexeme'] == 'variaveis':
                    self.match('variaveis')
                    if self.variaveis():
                        return self.match('}')
                else:
                    symb = self.get_symbol(self.last_ide)
                    self.semanticError(symb, type=2)
                    return True
        return False

    def follow_exp(self):
        follow = self.follow()       
        i=1
        rel_log = art = False
        while follow['lexeme'] not in [';',',',')','}']:
            follow = self.follow(i)      
            if follow['type'] in ['REL','LOG']:
                rel_log=True
            elif follow['type'] == 'ART':
                art=True 
            i += 1
            if self.i+i >= len(self.input): break
        return rel_log, art

    def expressao(self):
        if self.tag_retorno['status']: self.tag_retorno['type'] = 'booleano'
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            rel_log, art = self.follow_exp()
            if art:
                if self.exparitmetica():
                    if self.match(')'):
                        return self.expressaocont()
            elif rel_log:
                if self.expressao():
                    if self.match(')'):
                        return self.expressaocont()
        elif self.lookahead['lexeme'] == '!':
            self.match('!')
            return self.expressaob()
        elif self.lookahead['lexeme'] == '-':
            follow = self.follow(2)
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            else:
                self.match('-')
                if self.negativo():
                    return self.expressaocont()
        elif self.lookahead['type'] == 'NRO':
            follow = self.follow()
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            else:
                self.nro()
                return self.expressaocont()
        elif self.lookahead['type'] == 'IDE':
            follow = self.follow()
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            else:
                if self.acessovar():
                    return self.expressaocont()
        elif self.bool():
            return self.expressaocont()
        elif self.char():
            return self.expressaocont()
        elif self.cadeia():
            return self.expressaocont()
        return False

    def expressaob(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            follow = self.follow()                
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            elif self.expressao():
                if self.match(')'):
                    return self.expressaocont()
        elif self.lookahead['type'] == 'IDE':
            follow = self.follow()
            if follow['type'] == 'ART':
                if self.exparitmetica():
                    return self.expressaocont()
            else:
                if self.acessovar():
                    return self.expressaocont()
        elif self.bool():
            return self.expressaocont()
        return False

    def expressaocont(self):
        if self.lookahead['type'] in ['REL', 'LOG']:
            self.match(self.lookahead['lexeme'])
            return self.expressao()
        return True
    
    def para(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            if self.acessovar():
                if self.match('='):
                    if self.expatribuicao():
                        if self.match(';'):
                            return self.paracont()
        return False

    def paracont(self):
        follow = self.follow()
        if self.lookahead['lexeme'] == 'IDE':
            if follow['lexeme'] == ';':
                self.acessovar()
                self.match(';')
                return self.parafim()
        if self.expressao():
            if self.match(';'):
                return self.parafim()
        return False

    def parafim(self):
        if self.lookahead['lexeme'] in ['++','--']:
            if self.expatribuicao():
                return self.function_cont()
        rel_log, art = self.follow_exp()
        if rel_log:
            if self.expressao():
                return self.function_cont()
        elif art:
            follow = self.follow()
            if follow['lexeme'] in ['++','--']:
                if self.expatribuicao():
                    return self.function_cont()
            elif self.exparitmetica():
                return self.function_cont()
        return False
    
    def function_cont(self):
        if self.match(')') and self.match('{'):
            if self.conteudo():
                return self.match('}')
        return False

    def enquanto(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            rel_log, art = self.follow_exp()
            if rel_log:
                if self.expressao():
                    return self.function_cont()
            elif art:
                if self.exparitmetica():
                    return self.function_cont()
            elif self.bool():
                return self.function_cont()
            elif self.acessovar():
                return self.function_cont()
        return False

    def funcao(self):
        self.function_parameters = []
        if self.lookahead['lexeme'] == 'vazio':
            self.match('vazio')
            self.last_type = 'vazio'
            if self.tipocont():
                if self.ide():
                    return self.funcaoinit()
        elif self.tipo():
            if self.tipocont():
                if self.ide():
                    return self.funcaoinit()
        return False

    def funcaoinit(self):
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            self.current_scope = "FUNC_"+self.last_ide
            function = [self.last_ide, self.last_type]
            if self.paraninit():
                self.last_ide = function[0]
                self.last_type = function[1]
                self.save_symbol('FUNCAO')
                if self.match('{'):
                    ans=True
                    if self.lookahead['lexeme'] == '}':
                        self.semanticError({'category':'FUNCAO', 'lexeme': self.last_ide}, type=2)
                    while(self.lookahead['lexeme'] != '}' and self.i < len(self.input)-1):
                        result = self.conteudo()
                        if not result:
                            self.error()
                            ans = result
                        #else:

                    # caso a função tenha tipo diferente de vazio mas n possua retorno
                    symbol = self.get_symbol_by_scope(self.current_scope)
                    if not self.tag_retorno['status']:
                        if symbol and symbol['type'] != 'vazio':
                            self.semanticError(symbol, type=15)      
                    self.remove_symbol(self.current_scope)
                    self.current_scope = "GLOBAL"
                    self.tag_retorno['status']=False
                    return ans and self.match('}')
        return False

    def tipocont(self):
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.match(']'):
                return self.vetormais()
        return True

    def vetormais(self):
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            if self.match(']'):
                return self.vetormaisum()
        return True

    def vetormaisum(self):
        if self.lookahead['lexeme'] == '[':
            self.match('[')
            return self.match(']')
        return True

    def paraninit(self):
        if self.tipo():
            if self.ide():
                self.function_parameters.append({"lexeme": self.last_ide, "type": self.last_type})
                return self.paraninitcont()
        elif self.lookahead['lexeme'] == ')':
            return self.match(')')
        return False

    def paraninitcont(self):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.paraninit()
        return self.match(')')

    def retorno(self):
        self.tag_retorno['status']=True
        symbol = self.get_symbol_by_scope(self.current_scope)
        type = ( 0 if symbol is None else 1)
        
        if self.lookahead['lexeme'] == ';':
            return self.match(';') 
        elif self.valor(type,symbol):
            # caso a função tenha tipo vazio e possua retorno
            # caso a função tenha retorno com tipo diferente do que foi declarada 
            if type and self.tag_retorno['type'] != symbol['type']:
                self.semanticError(symbol, type=14)
            return self.match(';')
        return False

    def chamadafuncao(self, symbol = None):
        if symbol:
            symbol["paran_current"] = 0
        else:
            self.semanticError({'lexeme': self.last_ide, 'category': 'FUNCAO'}, type=4)
        if self.lookahead['lexeme'] == '(':
            self.match('(')
            return self.paran(symbol)
        return False
    
    def paran(self, symbol = None):
        if self.lookahead['lexeme'] == ')':
            return self.match(')')
        return self.parancont(symbol)

    def parancont(self, symbol = None):
        if self.valor(type=2, symbol=symbol):
            return self.paranfim(symbol)
        return False

    def paranfim(self, symbol = None):
        if self.lookahead['lexeme'] == ',':
            self.match(',')
            return self.parancont(symbol)
        elif self.lookahead['lexeme'] == ')':
            if symbol:
                symbol.pop("paran_current", None)
            return self.match(')')