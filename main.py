from recomendacao import avaliacoes_filme, avaliacoes_usuario
from math import sqrt


def euclidiana(base, usuario_1, usuario_2):
    si = {}

    for item in base[usuario_1]:
        if item in base[usuario_2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    soma = sum([pow(int(base[usuario_1][item]) - int(base[usuario_2][item]), 2)
                for item in base[usuario_1] if item in base[usuario_2]])

    return 1 / (1 + sqrt(soma))


def get_similares(base, usuario):
    similaridade = [(euclidiana(base, usuario, outro), outro)
                    for outro in base if outro != usuario]

    similaridade.sort(reverse=True)

    return similaridade[0:30]


def get_recomendacoes(base, usuario):
    totais = {}
    soma_similaridade = {}

    for outro in base:
        if outro == usuario:
            continue

        similaridade = euclidiana(base, usuario, outro)

        if similaridade <= 0:
            continue

        for item in base[outro]:
            if item not in base[usuario]:
                totais.setdefault(item, 0)
                totais[item] += base[outro][item] * similaridade
                soma_similaridade.setdefault(item, 0)
                soma_similaridade[item] += similaridade

    rankings = [(total / soma_similaridade[item], item)
                for item, total in totais.items()]

    rankings.sort(reverse=True)

    return rankings[0:30]


def carregar_movie_lens(path='ml-100k'):
    filmes = {}

    for linha in open(path + '/u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo

    base = {}

    for linha in open(path + '/u.data'):
        (usuario, id_filme, nota) = linha.split("\t")[0:3]
        base.setdefault(usuario, {})
        base[usuario][filmes[id_filme]] = nota
    return base

dados = carregar_movie_lens()

for itens in get_similares(dados, '1'):
    print(f'{itens[1]} - {itens[0]:.2f}')
