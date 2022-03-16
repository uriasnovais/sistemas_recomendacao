from recomendacao import avaliacoes_usuario as avaliacoes
from math import sqrt


def euclidiana(usuario_1, usuario_2):
    si = {}

    for item in avaliacoes[usuario_1]:
        if item in avaliacoes[usuario_2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    soma = sum([pow(avaliacoes[usuario_1][item] - avaliacoes[usuario_2][item], 2)
                for item in avaliacoes[usuario_1] if item in avaliacoes[usuario_2]])

    return 1 / (1 + sqrt(soma))


def get_similares(usuario):
    similaridade = [(euclidiana(usuario, outro), outro)
                    for outro in avaliacoes if outro != usuario]

    similaridade.sort(reverse=True)

    return similaridade


def get_recomendacoes(usuario):
    totais = {}
    soma_similaridade = {}

    for outro in avaliacoes:
        if outro == usuario:
            continue

        similaridade = euclidiana(usuario, outro)

        if similaridade <= 0:
            continue

        for item in avaliacoes(outro):
            if item not in avaliacoes[usuario]:
                totais.setdefault(item, 0)
                totais[item] += avaliacoes[outro][item] * similaridade
                soma_similaridade.setdefault(item, 0)
                soma_similaridade[item] += similaridade

    rankings = [(total / soma_similaridade[item], item)
                for item, total in totais.items()]

    rankings.sort(reverse=True)

    return rankings
