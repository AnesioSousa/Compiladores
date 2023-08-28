import re


def read_lines(filename):
    # o modo de leitura padrão é o "r"
    with open(filename) as file:
        for line in file:
            yield line


filename = "./files/outputs/saida_exemplo_teste_lexico.txt"
pattern = r"^(\d{2})\s([A-Z]{3})\s(.+)$"
unique_letters = set()


if __name__ == "__main__":
    for line in read_lines(filename):
        if re.match(pattern, line):
            unique_letters.update([char for char in line if char.isalpha()])

    print(len(unique_letters))
