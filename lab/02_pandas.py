"""
MÓDULO 02 · Pandas — dados tabulares e análise
==============================================

A ferramenta do dia a dia em Ciência de Dados.

Rode assim:

    uv run lab/02_pandas.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

# Onde estão os dados desta aula (caminho relativo a ESTE arquivo, para o
# script funcionar de qualquer pasta que você chame).
DADOS = Path(__file__).parent / "dados" / "produtos.csv"

print("=" * 66)
print("02 · PANDAS")
print("=" * 66)


# ──────────────────────────────────────────────────────────────────────
# 2.1 · Series e DataFrame
# ──────────────────────────────────────────────────────────────────────
# Duas estruturas, uma relação simples: um DataFrame é um conjunto de
# Series que compartilham o mesmo índice.

print("\n--- 2.1 · Series (uma coluna com índice) ---")

vendas = pd.Series([100, 150, 90], name="vendas")
print(vendas)

print("\n--- 2.1 · DataFrame (tabela com linhas e colunas) ---")

dados = {
    "produto": ["A", "B", "C"],
    "vendas": [100, 150, 90],
}
df = pd.DataFrame(dados)
print(df)

# Na prática os dados vêm de arquivos e bancos:
#   pd.read_csv()  ·  pd.read_excel()  ·  pd.read_sql()  ·  pd.read_json()


# ──────────────────────────────────────────────────────────────────────
# 2.2 · Selecionar e filtrar
# ──────────────────────────────────────────────────────────────────────

print("\n--- 2.2 · Selecionar uma coluna ---")
print(df["vendas"])

print("\n--- 2.2 · Filtrar linhas ---")
print(df[df["vendas"] > 100])

# POR QUE O FILTRO FUNCIONA?
# df["vendas"] > 100 devolve [False, True, False] — a MESMA máscara
# booleana do NumPy que vimos no módulo 01. O Pandas devolve apenas as
# linhas marcadas como True.
print("\na máscara por trás do filtro:")
print(df["vendas"] > 100)


# ──────────────────────────────────────────────────────────────────────
# 2.3 · Lendo os dados de verdade (CSV)
# ──────────────────────────────────────────────────────────────────────
# Daqui em diante usamos o catálogo de produtos que a nossa API vai
# publicar no módulo 06. É o mesmo dado percorrendo a pilha inteira.

print("\n--- 2.3 · pd.read_csv() ---")

produtos = pd.read_csv(DADOS)
print(produtos)
print("\ntipos de cada coluna (dtypes):")
print(produtos.dtypes)


# ──────────────────────────────────────────────────────────────────────
# 2.4 · Estatísticas e agrupamentos
# ──────────────────────────────────────────────────────────────────────

print("\n--- 2.4 · Estatística de uma coluna ---")
print("preço médio :", produtos["preco"].mean())

print("\ndescribe() — o resumo de sempre:")
print(produtos["preco"].describe())

print("\n--- 2.4 · Agrupar e somar (split · apply · combine) ---")

# Vamos acrescentar uma quarta linha ao catálogo para o agrupamento ficar
# interessante — duas categorias com dois produtos cada.
teclado = pd.DataFrame(
    [{"produto": "Teclado", "categoria": "Acessórios", "preco": 90, "vendas": 210}]
)
catalogo = pd.concat([produtos, teclado], ignore_index=True)
print(catalogo)

print("\ncatalogo.groupby('categoria')['preco'].sum()")
print(catalogo.groupby("categoria")["preco"].sum())

# split   → quebra a tabela por categoria
# apply   → aplica a função (sum) em cada grupo
# combine → junta tudo em um resultado

print("\nvárias contas de uma vez (agg):")
print(
    catalogo.groupby("categoria").agg(
        itens=("produto", "count"),
        preco_total=("preco", "sum"),
        preco_medio=("preco", "mean"),
    )
)


# ──────────────────────────────────────────────────────────────────────
# 2.5 · NumPy x Pandas — não são concorrentes
# ──────────────────────────────────────────────────────────────────────
# O Pandas se apoia no ecossistema NumPy: vetorização, máscaras booleanas
# e dtypes vêm de lá. Dá para descer ao NumPy a qualquer momento.

print("\n--- 2.5 · Descendo do Pandas para o NumPy ---")

precos = catalogo["preco"].to_numpy()      # a coluna vira um array NumPy
print("array          :", precos, type(precos).__name__)
print("média (NumPy)  :", precos.mean())
print("média (Pandas) :", catalogo["preco"].mean())

# Uma coluna nova calculada de forma vetorizada — sem laço nenhum:
catalogo["faturamento"] = catalogo["preco"] * catalogo["vendas"]
print("\ncoluna nova, calculada de uma vez para todas as linhas:")
print(catalogo[["produto", "preco", "vendas", "faturamento"]])

print("\nproduto mais caro   :", catalogo.loc[catalogo["preco"].idxmax(), "produto"])
print("produto que mais fatura:", catalogo.loc[catalogo["faturamento"].idxmax(), "produto"])
print("faturamento total (NumPy):", np.sum(catalogo["faturamento"].to_numpy()))


# ──────────────────────────────────────────────────────────────────────
# 2.6 · E AGORA PELA API — a tabela virando endpoint
# ──────────────────────────────────────────────────────────────────────
# O catálogo que lemos com pd.read_csv() é exatamente o que a nossa API
# publica. E o groupby acima tem um endpoint só dele.
#
#     uv run uvicorn main:app --reload

print("\n--- 2.6 · o mesmo Pandas, agora pela API ---")

import os  # noqa: E402

import requests  # noqa: E402

URL_BASE = os.getenv("URL_BASE", "http://127.0.0.1:8000")

try:
    # A tabela inteira, em JSON — é isto que o módulo 05 vai consumir.
    r = requests.get(f"{URL_BASE}/produtos", timeout=3)
    r.raise_for_status()
    print(f"GET {URL_BASE}/produtos")
    print(pd.DataFrame(r.json())[["id", "produto", "categoria", "preco"]])

    # E o groupby, servido:
    r = requests.get(f"{URL_BASE}/produtos/por-categoria", timeout=3)
    r.raise_for_status()
    print(f"\nGET {URL_BASE}/produtos/por-categoria")
    for categoria, dados_categoria in r.json().items():
        print(f"  {categoria:<14} {dados_categoria}")

    print("\nO servidor ainda não tem o Teclado — por isso os números não")
    print("batem com o bloco 2.4. Cadastre-o em POST /produtos e volte aqui:")
    print("o groupby passa a dar Acessórios 240 / Informática 5700.")
except requests.exceptions.RequestException:
    print("(API fora do ar — suba com `uv run uvicorn main:app --reload`)")


print("\n" + "=" * 66)
print("Resumo: NumPy calcula; Pandas organiza. A tabela é onde a análise")
print("acontece — e, servida por um endpoint, ela sai da sua máquina.")
print("Próximo: lab/03_visualizacao.py")
print("=" * 66)
