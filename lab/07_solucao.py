"""
MÓDULO 07 · Exercício integrado — SOLUÇÃO
=========================================

A solução comentada do desafio de lab/07_exercicio.py.
Tente o exercício antes de ler isto. :)

Rode assim:

    uv run lab/07_solucao.py
"""

import os
from pathlib import Path

import matplotlib

TEM_TELA = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
if not TEM_TELA:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import requests  # noqa: E402

URL_BASE = os.getenv("URL_BASE", "http://127.0.0.1:8000")
SAIDA = Path(__file__).parent / "saida"
SAIDA.mkdir(exist_ok=True)

DADOS_OFFLINE = [
    {"produto": "Notebook", "preco": 4500},
    {"produto": "Mouse", "preco": 150},
    {"produto": "Monitor", "preco": 1200},
]

print("=" * 66)
print("07 · SOLUÇÃO")
print("=" * 66)


# ──────────────────────────────────────────────────────────────────────
# PARTE 1 · OBTER E TRANSFORMAR
# ──────────────────────────────────────────────────────────────────────

print("\n--- passo 1 · obter com requests ---")

try:
    resposta = requests.get(f"{URL_BASE}/produtos", timeout=5)
    resposta.raise_for_status()
    dados = resposta.json()
    print(f"dados da API ({URL_BASE})")
except requests.exceptions.RequestException:
    dados = DADOS_OFFLINE
    print("API fora do ar — plano B: a lista em Python")

print("\n--- passo 2 · transformar em DataFrame ---")

df = pd.DataFrame(dados)
print(df[["produto", "preco"]])


# ──────────────────────────────────────────────────────────────────────
# PARTE 2 · CALCULAR
# ──────────────────────────────────────────────────────────────────────

print("\n--- passo 3 · preço médio ---")

media = df["preco"].mean()
print(f"preço médio: R$ {media:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

print("\n--- passo 4 · produto mais caro ---")

# idxmax() devolve o ÍNDICE da linha com o maior valor.
# df.loc[índice] devolve a linha inteira — não só o preço.
mais_caro = df.loc[df["preco"].idxmax()]
nome = mais_caro["produto"]
print(f"produto mais caro: {nome} (R$ {mais_caro['preco']:,.0f})".replace(",", "."))


# ──────────────────────────────────────────────────────────────────────
# PARTE 3 · VISUALIZAR
# ──────────────────────────────────────────────────────────────────────

print("\n--- passo 5 · gráfico de barras ---")

plt.bar(df["produto"], df["preco"], color="#2dd4bf")
plt.title("Preço por Produto")
plt.ylabel("Preço (R$)")
plt.tight_layout()

caminho = SAIDA / "07_solucao.png"
plt.savefig(caminho, dpi=120)
print(f"salvo: {caminho}")
if TEM_TELA:
    plt.show()
plt.close()


# ──────────────────────────────────────────────────────────────────────
# PARTE 4 · DISPONIBILIZAR
# ──────────────────────────────────────────────────────────────────────
# O passo 6 do enunciado — e ele já existe de verdade, em main.py:
#
#     @app.get("/produtos/media")
#     def preco_medio():
#         media = catalogo["preco"].mean()
#         return {"preco_medio": float(media)}
#
#     GET /produtos/media  →  {"preco_medio": 1950.0}
#
# Repare no float(): o Pandas devolve np.float64, e o JSON quer um número
# do Python. É o tipo de detalhe que só aparece quando se PUBLICA.

print("\n--- passo 6 · disponibilizar ---")
print("o endpoint já existe em main.py:")
print('    @app.get("/produtos/media")  →  {"preco_medio": %.1f}' % media)

try:
    r = requests.get(f"{URL_BASE}/produtos/media", timeout=5)
    print(f"    conferindo ao vivo: {r.status_code} {r.json()}")
except requests.exceptions.RequestException:
    print("    (suba a API com `uv run uvicorn main:app --reload` para conferir)")

print("\n" + "=" * 66)
print("O ciclo fechou: a API entregou JSON, o Pandas fez a tabela, o")
print("NumPy/Pandas calculou, o Matplotlib desenhou — e o resultado")
print("voltou a ser API. Ciência de Dados não termina no DataFrame.")
print("=" * 66)
