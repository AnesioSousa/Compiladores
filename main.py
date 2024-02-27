from app.lexer import LexicalAnalyser
from app.parser import GoatParser
import os


def main():
    myLexer = LexicalAnalyser()
    files = [f for f in os.listdir("./files") if f.endswith('.txt')]

    for file_name in files:
        file_path = os.path.join("./files", file_name)
        tokens = myLexer.scanner(file_path)

        myParser = GoatParser(file_name.removesuffix(
            '.txt'), input_sequence=tokens)

        myParser.program()
        if myParser.semanticStatus:
            print("Sucesso")


main()
