"""
MÓDULO 07 · Exercício integrado — junte tudo em um único script
===============================================================

DESAFIO
-------
Uma API devolve a seguinte lista de produtos:

    [
      {"produto": "Notebook", "preco": 4500},
      {"produto": "Mouse",    "preco": 150},
      {"produto": "Monitor",  "preco": 1200}
    ]

SUA TAREFA
----------
    1. Fazer a requisição com requests
    2. Transformar a resposta em DataFrame
    3. Calcular o preço médio
    4. Identificar o produto mais caro
    5. Criar um gráfico de barras
    6. Imaginar um endpoint FastAPI que disponibilize o preço médio

DICA
----
Se não houver uma API no ar, comece com a lista já em Python — este
arquivo faz isso sozinho. O foco do exercício é o ENCADEAMENTO das
etapas, não a rede.

Se você já cadastrou produtos com POST /produtos, reinicie o servidor
para o catálogo voltar aos três produtos do enunciado (o "banco" é um
DataFrame em memória — ele não sobrevive ao restart, e isso é de
propósito).

Rode assim:

    uv run lab/07_exercicio.py

A solução comentada está em lab/07_solucao.py — tente antes de olhar.
"""

import os
from pathlib import Path

import matplotlib

TEM_TELA = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
if not TEM_TELA:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (usado no passo 5)
import pandas as pd  # noqa: E402
import requests  # noqa: E402

URL_BASE = os.getenv("URL_BASE", "http://127.0.0.1:8000")
SAIDA = Path(__file__).parent / "saida"
SAIDA.mkdir(exist_ok=True)

# O plano B do enunciado: os dados já em Python, caso a API não esteja no ar.
DADOS_OFFLINE = [
    {"produto": "Notebook", "preco": 4500},
    {"produto": "Mouse", "preco": 150},
    {"produto": "Monitor", "preco": 1200},
]


def obter_dados() -> list[dict]:
    """PASSO 1 — buscar os dados na API, com plano B se ela não responder."""
    try:
        resposta = requests.get(f"{URL_BASE}/produtos", timeout=5)
        resposta.raise_for_status()
        print(f"✅ dados vieram da API ({URL_BASE})")
        return resposta.json()
    except requests.exceptions.RequestException:
        print("⚠️  API fora do ar — usando a lista em Python (plano B do enunciado)")
        return DADOS_OFFLINE


print("=" * 66)
print("07 · EXERCÍCIO INTEGRADO")
print("=" * 66)

dados = obter_dados()


# ──────────────────────────────────────────────────────────────────────
# PASSO 2 · Transformar a resposta em DataFrame
# ──────────────────────────────────────────────────────────────────────
# TODO: crie um DataFrame a partir de `dados` e imprima.
#
#   df = ...

df = None  # <- troque isto

if df is None:
    print("\n👉 Passo 2 pendente: crie o DataFrame e apague o `df = None`.")
    print("   Dica: pd.DataFrame(dados)")
    raise SystemExit(0)


# ──────────────────────────────────────────────────────────────────────
# PASSO 3 · Calcular o preço médio
# ──────────────────────────────────────────────────────────────────────
# TODO:
#   media = ...


# ──────────────────────────────────────────────────────────────────────
# PASSO 4 · Identificar o produto mais caro
# ──────────────────────────────────────────────────────────────────────
# TODO: use idxmax() para achar a LINHA do maior preço.
#   mais_caro = df.loc[...]
#   nome = ...


# ──────────────────────────────────────────────────────────────────────
# PASSO 5 · Criar um gráfico de barras
# ──────────────────────────────────────────────────────────────────────
# TODO:
#   plt.bar(...)
#   plt.title("Preço por Produto")
#   plt.ylabel("Preço (R$)")
#   plt.savefig(SAIDA / "07_exercicio.png")


# ──────────────────────────────────────────────────────────────────────
# PASSO 6 · Imaginar o endpoint FastAPI
# ──────────────────────────────────────────────────────────────────────
# Não precisa rodar — escreva no papel (ou aqui embaixo, como comentário)
# o endpoint que devolveria o preço médio:
#
#   @app.get("/produtos/media")
#   def preco_medio():
#       ...
#
# Depois compare com o que já existe em main.py, seção 4.3.
