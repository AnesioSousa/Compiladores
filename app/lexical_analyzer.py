class LexicalAnalyser:
    def __init__(self):
        self.__token_list = []
        # Matriz de transição
        self.__transition = {
            # [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,     27, 28]
            # [ L,	D,	_,	+,	-,	*,	/,	!,	=,	<,	&,	|,	>,	;,	,,	.,	(,	),	[,	],	{,	},	",	 , \n, \t, outros, EOF]
            0: [ 1, 3,  0,  8, 12, 17, 18, 25, 28, 31, 37, 40, 34, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,  0,  0,  0,     41,   0],
            1: [ 1, 1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54,  2,  2,  2,     41,   0],
            2: [ 2, 2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 41, 41,     41,   0],

        }
        self.__reserved_words = [
            "variables", "const", "class", "methods",
            "objects", "main", "return", "if", "else",
            "then", "for", "read", "print", "void", "int",
            "real", "boolean", "string", "true", "false"
        ]
        self.__final_states = {
            54: "IDE", 55: "IMF", 41: "TMF"
            
            f"{linha} {self.__final_states[]}"
        }
        self.__retro_states = [54, 55]

    def __get_column(self, character):
        
        
        pass

    # Generator
    def __read_lines(self, filename):
        # o modo de leitura padrão é o "r"
        with open(filename) as file:
            for line in file:
                yield line

    def scanner(self, path_to_input_file):
        line_counter = 1
        current_state = 0

        for line in self.__read_lines(path_to_input_file):
            lexeme = ""
            char_counter = 0
            while char_counter < len(line):
                char = line[char_counter]
                lexeme += char
                coluna = self.__get_column(char)
                current_state = self.__transition[int(
                    current_state)][int(coluna)]
                #Verifico as chaves ?
                if current_state in self.__final_states:
                    if current_state in self.__retro_states:
                        char_counter -= 1
                        lexeme = lexeme[:-1].strip()
                    self.__token_list.append(line_counter, current_state, lexeme)
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
    my_analyser.scanner("../files/inputs/entrada_exemplo_teste_lexico.txt")
