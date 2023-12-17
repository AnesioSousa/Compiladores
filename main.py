from app.lexer import LexicalAnalyser
from app.parser import GoatParser


def main():
    myLexer = LexicalAnalyser()

    tokens = myLexer.scanner("./files/other_input.txt")

    myParser = GoatParser(input_tokens=tokens)

    if myParser.program():
        print("SuCelso")
    else:
        print("Fail!")


main()
