class LexicalAnalyser:
    def __init__(self):
        self.__matriz = []
    
    def __get_coluna(self, character):
        pass
    
    def scanner(self, path_to_input_file):
        input_file = open(path_to_input_file)
        line = ''
        text = input_file.readlines()
        #Estado inicial
        state = 0
        i = 0
        for line in text:
            char_counter = 0
            while i < len(line):
                char = line[i]
                print(char)
                i += 1
if __name__  == '__main__':
    my_analyser = LexicalAnalyser()
    my_analyser.scanner('./files/inputs/entrada_exemplo_teste_lexico.txt')
