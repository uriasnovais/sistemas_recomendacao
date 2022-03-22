from recomendacao import avaliacoesUsuario as avaliacoes_usuario, avaliacoesFilme as avaliacoes_filme


def carregar_lista_usuario_filmes_nota(path='ml-100k'):
    filmes = {}

    for linha in open(path + "/u.item"):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo

    base_usuario_filmes_nota = {}

    for linha in open(path + '/u.data'):
        (usuario, id_filme, nota) = linha.split("\t")[0:3]
        base_usuario_filmes_nota.setdefault(usuario, {})
        base_usuario_filmes_nota[usuario][filmes[id_filme]] = nota
    return base_usuario_filmes_nota


def carregar_lista_filmes_usuario_nota(path='ml-100k'):
    filmes = {}

    for linha in open(path + "/u.item"):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo

    base_usuario_filmes_nota = {}

    for linha in open(path + '/u.data'):
        (usuario, id_filme, nota) = linha.split("\t")[0:3]
        base_usuario_filmes_nota.setdefault(filmes[id_filme], {})
        base_usuario_filmes_nota[filmes[id_filme]][usuario] = nota
    return base_usuario_filmes_nota


def distancia_euclidiana(base_dados, usuario_1, usuario_2):

    for item in base_dados[usuario_1]:
        if item in base_dados[usuario_2]:
            break
    else:
        return 0

    pp = 0

    for filme, nota in base_dados[usuario_1].items():
        if filme in base_dados[usuario_2]:
            item_1 = float(base_dados[usuario_1][filme])
            #print("1", filme,base_dados[usuario_1][filme]) #Teste de Paridade
            item_2 = float(base_dados[usuario_2][filme])
            #print("2", filme, base_dados[usuario_2][filme]) #Teste de Paridade
            produto_quadrado = (item_1 - item_2) ** 2
            pp += produto_quadrado
    raiz = 1/(1 + (pp ** 0.5))
    return raiz


def similaridade_total_usuarios(base_dados_usuario, usuario):
    similaridade = []
    for outro_usuario in base_dados_usuario:
        if outro_usuario != usuario:
            similaridade.append((distancia_euclidiana(base_dados_usuario, usuario, outro_usuario), outro_usuario))
    similaridade.sort(reverse=True)
    return similaridade


def similares_total_itens(base):
    resultado = {}
    for item in base:
        notas = similaridade_total_usuarios(base, item)
        print(notas)
        #if float(notas[0]) <= 0:
            #continue
        #resultado[item] = notas
    return resultado


def recomendacao_usuario_filmes(base_dados_usuario, usuario):
    recomendacoes_totais = {}
    soma_similaridade = {}

    for pessoa in base_dados_usuario:
        if pessoa == usuario:
            continue

        similaridade = distancia_euclidiana(base_dados_usuario, usuario, pessoa)

        if similaridade <= 0:
            continue

        for item in base_dados_usuario[pessoa]:
            if item not in base_dados_usuario[usuario]:
                recomendacoes_totais.setdefault(item, 0)
                recomendacoes_totais[item] += float(base_dados_usuario[pessoa][item]) * float(similaridade)
                soma_similaridade.setdefault(item, 0)
                soma_similaridade[item] += similaridade

    rankings = []
    for item, total in recomendacoes_totais.items():
        rankings.append([(total / soma_similaridade[item]), item])

    rankings.sort(reverse=True)

    return rankings


base_usuarios_movies = carregar_lista_usuario_filmes_nota()
base_movie_usuarios = carregar_lista_filmes_usuario_nota()

print(similares_total_itens(base_movie_usuarios))