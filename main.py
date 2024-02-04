from app.lexer import LexicalAnalyser
from app.parser import GoatParser

"""
def main():
    myLexer = LexicalAnalyser()
    files = [f for f in os.listdir("./files") if f.endswith('.txt')]
    
    for file_name in files:
        file_path = os.path.join("./files", file_name)
        tokens = myLexer.scanner(file_path)

        myParser = GoatParser(file_name.removesuffix('.txt'), input_tokens=tokens)

        if myParser.program():
            print("Sucesso")
        else:
            print("Falha")
"""


def main():
    myLexer = LexicalAnalyser()


    token_sequence = myLexer.scanner(path='./files/other_input.txt')
    myParser = GoatParser(token_sequence)

    if myParser.program():
        print("Sucesso")
    else:
        print("Falha")


main()
