class LexicalAnalyser:
    def __init__(self):
        self.__token_list = []
        self.__error_list = []
        # Matriz de transição ---9,  9,  
        self.__transition = {
            #  [0, 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,     26,  27]
            #  [L, D,  _,  +,  -,  *,  /,  !,  =,  <,  &,  |,  >,  ;,  ,,  .,  (,  ),  [,  ],  {,  },  ",   , \n, \t, outros, EOF]
            0: [1, 3,  0,  8, 12, 17, 18, 25, 28, 31, 37, 40, 34, 16, 16, 16, 16, 16, 16, 16, 16, 16, 51,  0,  0,  0,     41,   0],
            1: [1, 1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54,  2,  2,      2,   0],
            2: [2, 2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 41, 41,      2,   0],
            3: [56,3,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  5,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,      4,   0],
            5: [56,6, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56,     56,   0],
            6: [56,6,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,      7,   0],
            8: [9, 9,  9, 11,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,      9,   0],
           12: [13,13,13, 13, 11, 13, 13, 13, 13, 13, 13, 13, 16, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,     13,   0],
           
            
        }
        self.__reserved_words = [
            "variables", "const", "class", "methods",
            "objects", "main", "return", "if", "else",
            "then", "for", "read", "print", "void", "int",
            "real", "boolean", "string", "true", "false"
        ]
        
        self.__exit_states = {
            54: "IDE",   16: "DEL", 52: "CAC", 7: "NRO", 27:"REL", 26:"LOG", 9: "ART", 4: "NRO", 11:"ART"
        }
        self.__error_states = {
            53: "CMF", 56: "NMF", 57: "CoMF", 41: "TMF", 55: "IMF",
        }
        # Não tô lidando com números negativos!!!
        # NRO, ART, REL e LOG podem ser retrocessos ou não! - Possível solução: Tomar como estados diferentes. (gera mais estados no final)
        self.__retro_states = [54, 55, 26, 4, 9]

    def token_list(self):
        return self.__token_list

    def __get_column(self, character):
        ascii_value = ord(character)
        if (ascii_value >= 65 and ascii_value <= 90) or (ascii_value >= 97 and ascii_value <= 122):
            return 0
        elif ascii_value >= 48 and ascii_value <= 57:
            return 1
        elif character == "_":
            return 2
        elif character == "+":
            return 3
        elif character == "-":
            return 4
        elif character == "*":
            return 5
        elif character == "/":
            return 6
        elif character == "!":
            return 7
        elif character == "=":
            return 8
        elif character == "<":
            return 9
        elif character == "&":
            return 10
        elif character == "|":
            return 11
        elif character == ">":
            return 12
        elif character == ";":
            return 13
        elif character == ",":
            return 14
        elif character == ".":
            return 15
        elif character == "(":
            return 16
        elif character == ")":
            return 17
        elif character == "[":
            return 18
        elif character == "]":
            return 19
        elif character == "{":
            return 20
        elif character == "}":
            return 21
        elif character == '"':
            return 22
        elif character == " ":
            return 23
        elif character == "\n":
            return 24
        elif character == "\t":
            return 25
        else:
            return 26

    # Generator

    def __read_lines(self, filename):
        # o modo de leitura padrão é o "r"
        with open(filename, 'r') as file:
            for line in file:
                yield line

    def scanner(self, path_to_input_file):
        line_counter = 1
        current_state = 0
        lexeme = ""

        for line in self.__read_lines(path_to_input_file):
            char_counter = 0
            while char_counter < len(line):
                char = line[char_counter]
                lexeme += char
                coluna = self.__get_column(char)
                print(f"Caractere: {char} - Indice coluna: {coluna} - Estado atual: {current_state}")

                current_state = self.__transition[int(current_state)][int(coluna)]

                if current_state in (self.__exit_states | self.__error_states):
                    if current_state in self.__retro_states:
                        char_counter -= 1
                        lexeme = lexeme[:-1].strip()

                    if current_state in self.__error_states:
                        self.__error_list.append(
                            {"{:02}".format(line_counter), self.__error_states[current_state], lexeme})
                    else:
                        self.__token_list.append(
                            {"{:02}".format(line_counter), self.__exit_states[current_state], lexeme})
                    current_state = 0
                    lexeme = ""
                char_counter += 1
            line_counter += 1


"""
Primeiro faz a lista de tokens
Depois grava essa lista num arquivo txt de saída
"""

# IDÉIA: Usar argparse aqui
if __name__ == "__main__":
    my_analyser = LexicalAnalyser()
    my_analyser.scanner("./entrada_exemplo_teste_lexico.txt")
    print(my_analyser.token_list())
