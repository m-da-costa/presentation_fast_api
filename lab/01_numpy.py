"""
MÓDULO 01 · NumPy — arrays e computação numérica
================================================

A base numérica de todo o ecossistema de dados em Python.

Rode assim:

    uv run lab/01_numpy.py

Este arquivo é para ser lido de cima para baixo enquanto roda. Cada bloco
corresponde a um slide da aula.
"""

import time

import numpy as np

def _cronometrar(funcao) -> float:
    """Roda a função uma vez e devolve quanto tempo levou, em segundos."""
    inicio = time.perf_counter()
    funcao()
    return time.perf_counter() - inicio


print("=" * 66)
print("01 · NUMPY")
print("=" * 66)


# ──────────────────────────────────────────────────────────────────────
# 1.1 · O problema que o NumPy resolve
# ──────────────────────────────────────────────────────────────────────
# Listas do Python são flexíveis, mas não foram feitas para cálculo
# numérico em massa. Compare as duas formas de "dobrar cada valor":

print("\n--- 1.1 · Python puro x NumPy ---")

# PYTHON PURO: precisamos de um laço e de uma lista auxiliar
valores_lista = [10, 20, 30]
dobro_lista = []
for v in valores_lista:
    dobro_lista.append(v * 2)
print("python puro:", dobro_lista)

# COM NUMPY: a operação vale para o array inteiro
valores = np.array([10, 20, 30])
dobro = valores * 2
print("com numpy  :", dobro)

# Mesma tarefa. Menos código, mais legível e MUITO mais rápido — porque a
# repetição acontece dentro de código compilado, não no laço do Python.


# ──────────────────────────────────────────────────────────────────────
# 1.2 · O ndarray: a estrutura central do NumPy
# ──────────────────────────────────────────────────────────────────────
# Um array n-dimensional, homogêneo (todos os elementos do mesmo tipo)
# e de tamanho fixo, guardado de forma contígua na memória.

print("\n--- 1.2 · O ndarray ---")

vetor = np.array([7.5, 8.0, 6.5])          # 1D — notas de um aluno
matriz = np.array([[1, 2], [3, 4]])        # 2D — uma tabela de valores
tensor = np.zeros((2, 3, 4))               # 3D — imagens, séries temporais

for nome, arr in [("vetor ", vetor), ("matriz", matriz), ("tensor", tensor)]:
    # shape = formato · dtype = tipo dos elementos · ndim = nº de dimensões
    print(f"{nome}  shape={arr.shape}  dtype={arr.dtype}  ndim={arr.ndim}")


# ──────────────────────────────────────────────────────────────────────
# 1.3 · Vetorização: a operação vale para o array inteiro
# ──────────────────────────────────────────────────────────────────────
# Sem laço. Sem índice. A operação se propaga elemento a elemento.

print("\n--- 1.3 · Vetorização ---")

print("valores       :", valores)
print("valores + 5   :", valores + 5)       # soma escalar a todos
print("valores * 2   :", valores * 2)       # multiplica todos
print("valores ** 2  :", valores**2)        # eleva todos ao quadrado
print("valores > 15  :", valores > 15)      # array de True / False (máscara)

a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print("a + b         :", a + b)             # soma elemento a elemento

# A máscara booleana é a mesma ideia que o Pandas usa para filtrar linhas.
# Guarde este nome — ele volta no módulo 02.
print("valores[valores > 15] :", valores[valores > 15])


# ──────────────────────────────────────────────────────────────────────
# 1.4 · Estatísticas básicas em uma linha
# ──────────────────────────────────────────────────────────────────────

print("\n--- 1.4 · Estatísticas ---")

notas = np.array([7.5, 8.0, 6.5, 9.0, 8.5])

print("notas          :", notas)
print("mean()   média :", notas.mean())
print("max()    maior :", notas.max())
print("min()    menor :", notas.min())
print("std()    desvio:", round(float(notas.std()), 4))
print("sum()    soma  :", notas.sum())
print("median() mediana:", np.median(notas))
print("argmax() posição do maior:", notas.argmax())


# ──────────────────────────────────────────────────────────────────────
# 1.5 · Por que usar NumPy em vez de listas? — a medição real
# ──────────────────────────────────────────────────────────────────────
# O slide promete uma medição: dobrar 1 milhão de elementos, lista contra
# array. Aqui ela acontece de verdade, na máquina de quem está rodando.

print("\n--- 1.5 · Medição real: dobrar 1 milhão de elementos ---")

N = 1_000_000

# O MESMO código do slide: laço explícito com append.
lista = list(range(N))
inicio = time.perf_counter()
dobro_py = []
for x in lista:
    dobro_py.append(x * 2)
tempo_lista = time.perf_counter() - inicio

# O MESMO código do slide: uma linha, sem laço.
# Repetimos 3 vezes e ficamos com o melhor tempo — a máquina de cada um
# tem ruído (outros programas rodando), e queremos medir o código.
array = np.arange(N)
tempo_numpy = min(
    _cronometrar(lambda: array * 2) for _ in range(3)
)

print(f"lista Python : {tempo_lista * 1000:8.2f} ms")
print(f"array NumPy  : {tempo_numpy * 1000:8.2f} ms")
print(f"NumPy foi ~{tempo_lista / tempo_numpy:.0f}x mais rápido")

# Memória: a lista guarda 1 milhão de PONTEIROS para 1 milhão de objetos
# int do Python. O array guarda 1 milhão de números, um do lado do outro.
print(f"\nmemória do array NumPy: {array.nbytes / 1024 / 1024:.1f} MB")



# ──────────────────────────────────────────────────────────────────────
# 1.6 · E AGORA PELA API — o mesmo cálculo, servido por HTTP
# ──────────────────────────────────────────────────────────────────────
# Este é o fio que costura a aula: tudo o que rodou acima vira endpoint na
# NOSSA API (main.py). Suba o servidor e rode este arquivo de novo:
#
#     uv run uvicorn main:app --reload
#
# Não é um extra — é o ponto. Um cálculo que só roda no seu terminal não
# serve a mais ninguém.

print("\n--- 1.6 · o mesmo NumPy, agora pela API ---")

import os  # noqa: E402

import requests  # noqa: E402

URL_BASE = os.getenv("URL_BASE", "http://127.0.0.1:8000")

try:
    resposta = requests.get(
        f"{URL_BASE}/numpy/estatisticas",
        params={"valores": "7.5,8.0,6.5,9.0,8.5"},
        timeout=3,
    )
    resposta.raise_for_status()
    print(f"GET {URL_BASE}/numpy/estatisticas?valores=7.5,8.0,6.5,9.0,8.5")
    for chave, valor in resposta.json().items():
        print(f"  {chave:<18} {valor}")
    print("\nMesmos números do bloco 1.4 — só que agora qualquer sistema")
    print("do mundo consegue pedir esse cálculo.")
except requests.exceptions.RequestException:
    print("(API fora do ar — suba com `uv run uvicorn main:app --reload`")
    print(" e rode este arquivo de novo para ver o mesmo cálculo por HTTP)")

print("\n" + "=" * 66)
print("Resumo: NumPy = desempenho, vetorização, multidimensional e a")
print("fundação em que Pandas, SciPy e scikit-learn se apoiam — e, servido")
print("por um endpoint, deixa de ser um cálculo e vira um SERVIÇO.")
print("Próximo: lab/02_pandas.py")
print("=" * 66)
