# Alfabeto
alfabeto = ['a', 'b']

# Matriz de transição
# Estados: q0 (inicial), q1, q2 (final)
# q0 -> Começo
# q1 -> Viu um '1'
# q2 -> Viu '10'
# Matriz de transição
transicao = [
    [0, 1],  # Transições do estado q0
    [2, 0],  # Transições do estado q1
    [0, 3],   # Transições do estado q2
    [4, 0], 
    [4, 0],
]


# Vetor de estados finais
finais = [0, 0, 0, 0, 1]

def reconhece_string(s):
    estado_atual = 0
    for char in s:
        # Encontrando o índice do caractere no alfabeto
        coluna = alfabeto.index(char)
        estado_atual = transicao[estado_atual][coluna]
    return finais[estado_atual] == 1

# Testando
print(reconhece_string("aaaaababaaaaaaaaaaa"))  # True
print(reconhece_string("abaa"))    # False
print(reconhece_string("ababaa")) # True
