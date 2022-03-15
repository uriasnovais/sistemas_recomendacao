from recomendacao import avaliacoes_usuario as avaliacoes, avaliacoes_usuario
from math import sqrt


def distancia_euclidiana(base, usuario_1, usuario_2):
    si = {}
    for item in base[usuario_1]:
        if item in base[usuario_2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    soma = sum([pow(base[usuario_1][item] - base[usuario_2][item], 2)
                for item in base[usuario_1] if item in base[usuario_2]])

    return 1 / (1 + sqrt(soma))


def similares(base, usuario):
    similaridade = [(distancia_euclidiana(base, usuario, outro), outro)
                    for outro in base if outro != usuario]
    similaridade.sort(reverse=True)
    return similaridade


comp_1 = similares(avaliacoes_usuario, 'Marcos')
print(f'Grau de Similaridade: \n{comp_1}')
