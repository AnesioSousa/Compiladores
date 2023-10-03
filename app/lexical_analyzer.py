import itertools


class LexicalAnalyser:
    def __init__(self):
        self.__token_list = []
        self.__error_list = []
        # Matriz de transição
        self.__transition = {
             #  [0,   1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,         26]
             #  [L,   D,  _,  +,  -,  *,  /,  !,  =,  <,  &,  |,  >,  ;,  ,,  .,  (,  ),  [,  ],  {,  },  ",   , \n, \t, indefinido]
             0: [ 1,  3,  0,  8, 12, 17, 18, 25, 28, 31, 37, 40, 34, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,         41],
             1: [ 1,  1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54,  2,  2,          2],
             2: [ 2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 41, 41,          2],
             3: [56,  3,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  5,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,          4],
             5: [56,  6, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56,         56],
             6: [58,  6, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58,  4,  4, 58,  4,  4,  4,  4,  4,  4, 58,  4, 58, 58,         58],
             8: [ 9,  9,  9, 11,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,          9],
            12: [ 9,  9,  9,  9, 11,  9,  9,  9,  9,  9,  9,  9, 16,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,          9],
            18: [ 9,  9,  9,  9,  9, 22, 20,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,  9,          9],
            20: [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 22, 20,  0, 20,         20],
            22: [57, 57, 57, 57, 57, 23, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57,         22],
            23: [57, 57, 57, 57, 57, 57,  0, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57,         57],
            25: [26, 26, 26, 26, 26, 26, 26, 26, 27, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,         26],
            28: [29, 29, 29, 29, 29, 29, 29, 29, 27, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29,         29],
            31: [29, 29, 29, 29, 29, 29, 29, 29, 27, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29,         29],
            34: [29, 29, 29, 29, 29, 29, 29, 29, 27, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29,         29],
            37: [41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 39, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41,         41],
            40: [41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 39, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41,         41],
            51: [51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 52, 51, 53, 51,         60],
            58: [58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 59, 59, 58, 59, 59, 59, 59, 59, 59, 58, 59, 58, 58,         58],
            60: [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 53, 60, 53, 60,         60],
        }
        self.__reserved_words = [
            "variables", "const", "class", "methods",
            "objects", "main", "return", "if", "else",
            "then", "for", "read", "print", "void", "int",
            "real", "boolean", "string", "true", "false",
            "true", "constructor"
        ]

        self.__exit_states = {
            54: "IDE",   16: "DEL", 52: "CAC", 7: "NRO", 27: "REL", 26: "LOG", 9: "ART", 4: "NRO", 11: "ART", 29: "REL", 39: "LOG"
        }
        self.__error_states = {
            53: "CMF", 56: "NMF", 57: "CoMF", 41: "TMF", 55: "IMF", 59: "NMF"
        }

        self.__retro_states = [54, 55, 26, 4, 9, 29, 59]

    def token_list(self):
        return self.__token_list

    def __get_column(self, character):
        #print(character)
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

    def __generate_output_files(self):
        with open("../files/saida.txt", 'w') as f:
            for token in self.__token_list:
                f.write(
                    f"{token['number_line']} {token['token_type']} {token['lexeme']}\n")
            f.write("\n")
            for token in self.__error_list:
                f.write(
                    f"{token['number_line']} {token['token_type']} {token['lexeme']}\n")

    def scanner(self, path_to_input_file):
        line_counter = 1
        current_state = 0
        lexeme = ""

        for line in self.__read_lines(path_to_input_file):
            #print(line, end='')
            char_counter = 0
            while char_counter < len(line):
                char = line[char_counter]
                print(char, end='')

                coluna = self.__get_column(char)
                current_state = self.__transition[int(current_state)][int(coluna)]

                if current_state in (self.__exit_states | self.__error_states):
                    if current_state in self.__retro_states:
                        char_counter -= 1
                        lexeme = lexeme[:-1].strip()

                    if current_state in self.__error_states:
                        self.__error_list.append({
                            "number_line": "{:02}".format(line_counter),
                            "token_type": self.__error_states[current_state],
                            "lexeme": lexeme
                        })
                    else:
                        self.__token_list.append({
                            "number_line": "{:02}".format(line_counter),
                            "token_type": "PRE" if lexeme in self.__reserved_words else self.__exit_states[current_state],
                            "lexeme": lexeme
                        })
                    current_state = 0
                    lexeme = ""
                    
                elif current_state == 0:
                    lexeme = ""
                char_counter += 1
            line_counter += 1
        
        #tem que veificar o estado atual aqui e atualizá-lo de acordo.
        #if current_state == 
        
        self.__generate_output_files()


if __name__ == "__main__":
    my_analyser = LexicalAnalyser()
    my_analyser.scanner("../files/codigos_teste_lexico_2023.2/teste01_identificadores.txt")
