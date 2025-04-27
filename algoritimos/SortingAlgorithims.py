import random
import datetime
import time
import heapq
import matplotlib.pyplot as plt

# 1. Preparação dos Dados
class Produto:
    def __init__(self, nome, preco, avaliacao, data_adicao, categoria):
        self.nome = nome
        self.preco = preco
        self.avaliacao = avaliacao
        self.data_adicao = data_adicao
        self.categoria = categoria
    
    def __repr__(self):
        return f"{self.nome}: Preço: {self.preco}, Avaliação: {self.avaliacao}, Data de Adição: {self.data_adicao}, Categoria: {self.categoria}"

# 2. Geração de Dados
def gerar_produtos(n):
    nomes = [f"Produto{i}" for i in range(n)]
    precos = [round(random.uniform(10, 1000), 2) for _ in range(n)]
    avaliacoes = [round(random.uniform(0, 5), 2) for _ in range(n)]
    datas = [datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365)) for _ in range(n)]
    categorias = [f"Categoria{random.randint(1, 5)}" for _ in range(n)]
    
    produtos = [Produto(nomes[i], precos[i], avaliacoes[i], datas[i], categorias[i]) for i in range(n)]
    return produtos

# 3. Implementação de Algoritmos de Ordenação

# 3.1 Bubble Sort
def bubble_sort(lista, key=lambda x: x):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if key(lista[j]) > key(lista[j+1]):
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

# 3.2 Quick Sort
def quick_sort(lista, key=lambda x: x):
    if len(lista) <= 1:
        return lista
    else:
        pivot = lista[0]
        less = [x for x in lista[1:] if key(x) <= key(pivot)]
        greater = [x for x in lista[1:] if key(x) > key(pivot)]
        return quick_sort(less, key) + [pivot] + quick_sort(greater, key)

# 3.3 Merge Sort
def merge_sort(lista, key=lambda x: x):
    if len(lista) <= 1:
        return lista
    
    mid = len(lista) // 2
    left = merge_sort(lista[:mid], key)
    right = merge_sort(lista[mid:], key)
    
    return merge(left, right, key)

def merge(left, right, key):
    sorted_list = []
    while left and right:
        if key(left[0]) <= key(right[0]):
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    sorted_list.extend(left if left else right)
    return sorted_list

# 3.4 Heap Sort
def heap_sort(lista, key=lambda x: x):
    # Cria uma lista de tuplas onde o primeiro elemento é a chave de ordenação
    heap = [(key(x), i, x) for i, x in enumerate(lista)]
    # Converte a lista em uma heap
    heapq.heapify(heap)
    # Extrai os elementos ordenados a partir da heap, ignorando a chave e mantendo a ordem estável
    return [heapq.heappop(heap)[2] for _ in range(len(heap))]

# 4. Critérios de Ordenação

def ordenar_por_preco(produtos, ascendente=True):
    return bubble_sort(produtos, key=lambda x: x.preco) if ascendente else bubble_sort(produtos, key=lambda x: -x.preco)

def ordenar_por_avaliacao(produtos, ascendente=True):
    return quick_sort(produtos, key=lambda x: x.avaliacao) if ascendente else quick_sort(produtos, key=lambda x: -x.avaliacao)

def ordenar_por_data_adicao(produtos, recente_primeiro=True):
    return merge_sort(produtos, key=lambda x: x.data_adicao) if recente_primeiro else merge_sort(produtos, key=lambda x: -x.data_adicao.timestamp())

def ordenar_por_categoria(produtos):
    return heap_sort(produtos, key=lambda x: x.categoria)

# 5. Comparação de Desempenho

def medir_tempo(func, *args):
    inicio = time.time()
    resultado = func(*args)
    fim = time.time()
    return resultado, fim - inicio

# 6. Análise de Resultados

def comparar_algoritmos(produtos):
    tempos = {}
    
    # Comparação por preço
    _, tempo_bubble = medir_tempo(ordenar_por_preco, produtos, True)
    tempos['Bubble Sort (Preço Asc)'] = tempo_bubble

    _, tempo_quick = medir_tempo(ordenar_por_avaliacao, produtos, True)
    tempos['Quick Sort (Avaliação Asc)'] = tempo_quick

    _, tempo_merge = medir_tempo(ordenar_por_data_adicao, produtos, True)
    tempos['Merge Sort (Data Recente)'] = tempo_merge

    _, tempo_heap = medir_tempo(ordenar_por_categoria, produtos)
    tempos['Heap Sort (Categoria)'] = tempo_heap

    return tempos

def plotar_tempos(tempos):
    plt.bar(tempos.keys(), tempos.values())
    plt.ylabel('Tempo (segundos)')
    plt.title('Comparação de Algoritmos de Ordenação')
    plt.xticks(rotation=45)
    plt.show()

# Geração de produtos
produtos = gerar_produtos(1000)

# Comparação de algoritmos
tempos = comparar_algoritmos(produtos)

# Exibição dos resultados
plotar_tempos(tempos)

# Exibir os tempos em console
for algoritmo, tempo in tempos.items():
    print(f"{algoritmo}: {tempo:.5f} segundos")
