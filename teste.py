class LexicalAnalyser:
    def __init__(self):
        self.__matriz = []
    
    def __get_column(self, character):
        pass
    
    #Generator
    def __read_lines(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                yield line
        
    def scanner(self, path_to_input_file):
        line_counter = 1;
        state = 0
        
        for line in self.__read_lines(path_to_input_file):
            print(line, end='')
            lexeme = ''
            char_counter = 0
            while char_counter < len(line):
                char = line[char_counter]
                lexeme += char
                coluna = self.__get_column(char)
                state = self.__matriz[int(state)][int(coluna)]
                if state in self.__estado_final:
                    if state in self.__estado_retrocesso:
                        char_counter-=1
                        lexeme = lexeme[:-1].strip()
                    self.__add_list_tokens(state,lexeme, line_counter)
                    state = 0
                    lexeme = ''
                char_counter += 1
                
# Usar argparse aqui
if __name__  == '__main__':
    my_analyser = LexicalAnalyser()
    my_analyser.scanner('./files/inputs/entrada_exemplo_teste_lexico.txt')
