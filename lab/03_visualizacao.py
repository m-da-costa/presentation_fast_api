"""
MÓDULO 03 · Matplotlib e Seaborn — visualização de dados
========================================================

Transformar números em entendimento. A estatística resume; o gráfico
revela o que o resumo esconde.

Rode assim:

    uv run lab/03_visualizacao.py

Os gráficos são salvos em lab/saida/*.png. Se você estiver numa máquina
com tela, eles também abrem em janelas.
"""

import os
from pathlib import Path

import matplotlib

# Se não há tela (servidor, terminal puro), desenhamos direto no arquivo.
# Numa máquina com ambiente gráfico, as janelas abrem normalmente.
TEM_TELA = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
if not TEM_TELA:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

AQUI = Path(__file__).parent
DADOS = AQUI / "dados" / "produtos.csv"
SAIDA = AQUI / "saida"
SAIDA.mkdir(exist_ok=True)

print("=" * 66)
print("03 · VISUALIZAÇÃO")
print("=" * 66)


def mostrar(nome: str) -> None:
    """Salva o gráfico atual em lab/saida/ e mostra na tela, se houver."""
    caminho = SAIDA / f"{nome}.png"
    plt.tight_layout()
    plt.savefig(caminho, dpi=120)
    print(f"  salvo: {caminho.relative_to(AQUI.parent)}")
    if TEM_TELA:
        plt.show()
    plt.close()


# ──────────────────────────────────────────────────────────────────────
# 3.1 · Matplotlib: controle sobre cada elemento
# ──────────────────────────────────────────────────────────────────────
# Cada chamada acrescenta uma camada ao gráfico: barras, título, rótulos.

print("\n--- 3.1 · Matplotlib: o gráfico de barras do slide ---")

produtos = ["A", "B", "C"]
vendas = [100, 150, 90]

plt.bar(produtos, vendas)
plt.title("Vendas por Produto")
plt.xlabel("Produto")
plt.ylabel("Vendas")
mostrar("31_barras_matplotlib")


# ──────────────────────────────────────────────────────────────────────
# 3.2 · Os quatro gráficos do dia a dia
# ──────────────────────────────────────────────────────────────────────
# A escolha do gráfico vem da PERGUNTA, não do gosto:
#   acompanhar no tempo → plot   ·  comparar categorias → bar
#   relacionar variáveis → scatter ·  ver a distribuição → hist

print("\n--- 3.2 · Os quatro gráficos do dia a dia ---")

# Dados de exemplo, gerados com NumPy (semente fixa = todo mundo vê o mesmo)
rng = np.random.default_rng(42)
meses = np.arange(1, 13)
faturamento = 50_000 + np.cumsum(rng.normal(2_000, 3_000, 12))
altura = rng.normal(1.72, 0.09, 300)
peso = 45 + (altura - 1.5) * 100 + rng.normal(0, 6, 300)

figura, eixos = plt.subplots(2, 2, figsize=(11, 7))

eixos[0, 0].plot(meses, faturamento, marker="o")
eixos[0, 0].set_title("plot() — evolução no tempo")
eixos[0, 0].set_xlabel("mês")

eixos[0, 1].bar(produtos, vendas)
eixos[0, 1].set_title("bar() — comparar categorias")

eixos[1, 0].scatter(altura, peso, alpha=0.5, s=14)
eixos[1, 0].set_title("scatter() — relação entre variáveis")
eixos[1, 0].set_xlabel("altura (m)")
eixos[1, 0].set_ylabel("peso (kg)")

eixos[1, 1].hist(altura, bins=20)
eixos[1, 1].set_title("hist() — distribuição de valores")
eixos[1, 1].set_xlabel("altura (m)")

figura.suptitle("Os quatro gráficos do dia a dia", fontsize=14)
mostrar("32_quatro_graficos")


# ──────────────────────────────────────────────────────────────────────
# 3.3 · Seaborn: alto nível e integrado ao Pandas
# ──────────────────────────────────────────────────────────────────────
# O Seaborn recebe o DataFrame INTEIRO e você indica as colunas pelo nome.
# Ele cuida de cores, legenda e rótulos.

print("\n--- 3.3 · Seaborn: data=df e os nomes das colunas ---")

df = pd.read_csv(DADOS)

sns.barplot(data=df, x="produto", y="preco", hue="categoria")
plt.title("Preço por Produto")
plt.ylabel("Preço (R$)")
mostrar("33_barras_seaborn")


# ──────────────────────────────────────────────────────────────────────
# 3.4 · Gráficos estatísticos com pouquíssimo código
# ──────────────────────────────────────────────────────────────────────
# Um restaurante: contas e gorjetas, por turno. Geramos os dados aqui
# mesmo — a aula roda sem internet.

print("\n--- 3.4 · boxplot e scatterplot ---")

n = 240
turno = rng.choice(["almoço", "jantar"], size=n, p=[0.45, 0.55])
conta = np.where(
    turno == "jantar",
    rng.gamma(shape=7.0, scale=9.0, size=n),
    rng.gamma(shape=5.0, scale=7.0, size=n),
)
gorjeta = conta * rng.normal(0.13, 0.04, n) + rng.normal(0, 0.4, n)

d = pd.DataFrame({"turno": turno, "conta": conta.round(2), "gorjeta": gorjeta.round(2)})
print(d.head())
print("\nresumo por turno:")
print(d.groupby("turno")[["conta", "gorjeta"]].mean().round(2))

figura, eixos = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(data=d, x="turno", y="conta", ax=eixos[0])
eixos[0].set_title("boxplot — distribuição da conta por turno")
sns.scatterplot(data=d, x="conta", y="gorjeta", hue="turno", ax=eixos[1])
eixos[1].set_title("scatterplot — conta x gorjeta")
mostrar("34_seaborn_estatistico")


# ──────────────────────────────────────────────────────────────────────
# 3.5 · Matplotlib x Seaborn: não são alternativas
# ──────────────────────────────────────────────────────────────────────
# O Seaborn desenha POR CIMA do Matplotlib. O padrão real de trabalho é:
# criar o gráfico com Seaborn e ajustar título, eixos e limites com
# Matplotlib — exatamente como abaixo.

print("\n--- 3.5 · Seaborn desenha, Matplotlib ajusta ---")

sns.set_theme(style="whitegrid")            # tema do Seaborn
eixo = sns.barplot(data=df, x="produto", y="preco", color="#2dd4bf")

plt.title("Catálogo — preço por produto", fontsize=14)   # Matplotlib
plt.ylabel("Preço (R$)")
plt.xlabel("")
plt.ylim(0, 5000)
for barra, preco in zip(eixo.patches, df["preco"], strict=True):
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        preco + 90,
        f"R$ {preco:,.0f}".replace(",", "."),
        ha="center",
        fontsize=10,
    )
mostrar("35_seaborn_mais_matplotlib")


# ──────────────────────────────────────────────────────────────────────
# 3.6 · E AGORA PELA API — o gráfico entregue por HTTP
# ──────────────────────────────────────────────────────────────────────
# Uma API não devolve só JSON. O endpoint /produtos/grafico desenha este
# mesmo gráfico no servidor e devolve os bytes de um PNG.
#
#     uv run uvicorn main:app --reload
#
# Abra http://127.0.0.1:8000/produtos/grafico direto no navegador.

print("\n--- 3.6 · o mesmo gráfico, agora pela API ---")

import requests  # noqa: E402

URL_BASE = os.getenv("URL_BASE", "http://127.0.0.1:8000")

try:
    r = requests.get(f"{URL_BASE}/produtos/grafico", timeout=5)
    r.raise_for_status()
    destino = SAIDA / "36_grafico_da_api.png"
    destino.write_bytes(r.content)
    print(f"GET {URL_BASE}/produtos/grafico")
    print(f"  Content-Type : {r.headers['content-type']}")
    print(f"  tamanho      : {len(r.content) / 1024:.1f} KB")
    print(f"  salvo em     : {destino.relative_to(AQUI.parent)}")
    print("\nNo servidor não existe tela: lá o Matplotlib usa o motor 'Agg'")
    print("e desenha direto na memória. Veja o comentário no topo do main.py.")
except requests.exceptions.RequestException:
    print("(API fora do ar — suba com `uv run uvicorn main:app --reload`)")


print("\n" + "=" * 66)
print("Resumo: o gráfico responde a uma pergunta. Matplotlib dá controle;")
print("Seaborn dá velocidade — e a API entrega o resultado a quem precisa.")
print("Próximo: lab/04_json_xml.py")
print("=" * 66)
