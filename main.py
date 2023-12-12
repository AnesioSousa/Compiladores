from app.lexer import LexicalAnalyser
from app.parser import GoatParser


def main():
    myLexer = LexicalAnalyser()

    tokens = myLexer.scanner("./teste-gramatica.txt")

    myParser = GoatParser(input_tokens=tokens)

    if myParser.run_program():
        print("SuCelso")
    else:
        print("Fail!")


main()
