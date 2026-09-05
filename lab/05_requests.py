"""
MÓDULO 05 · requests — consumindo APIs com Python
=================================================

Trazer dados do mundo real para dentro do Python.

ANTES DE RODAR, suba a API em outro terminal:

    uv run uvicorn main:app --reload

Depois, aqui:

    uv run lab/05_requests.py

Hoje somos os dois lados do balcão: a API que este script consome é a
mesma que vamos escrever no módulo 06. Para consumir uma API pública de
verdade, a ÚNICA coisa que muda é a variável URL_BASE lá embaixo.
"""

import os

import pandas as pd
import requests

# A URL da API. Um endereço público entraria exatamente aqui.
URL_BASE = os.getenv("URL_BASE", "http://127.0.0.1:8000")

print("=" * 66)
print("05 · REQUESTS")
print(f"consumindo: {URL_BASE}")
print("=" * 66)


# ──────────────────────────────────────────────────────────────────────
# 5.1 · A requisição mais simples possível
# ──────────────────────────────────────────────────────────────────────

print("\n--- 5.1 · requests.get() ---")

try:
    resposta = requests.get(f"{URL_BASE}/produtos", timeout=10)
except requests.exceptions.ConnectionError:
    print("\n  ❌ Não consegui falar com a API.")
    print("     Suba o servidor em outro terminal e rode de novo:")
    print("       uv run uvicorn main:app --reload\n")
    raise SystemExit(1) from None

# Os três atributos que você vai usar o tempo todo:
print("status_code :", resposta.status_code)   # o número do resultado
print("headers     :", resposta.headers["content-type"])
print("text (bruto):", resposta.text[:80], "…")
print("json()      :", resposta.json()[0])     # já é uma lista de dicts

# requests.get() · requests.post() · requests.put() · requests.delete()
# — uma função para cada método HTTP que vimos no módulo 04.


# ──────────────────────────────────────────────────────────────────────
# 5.2 · Do JSON ao DataFrame
# ──────────────────────────────────────────────────────────────────────
# Provavelmente o trecho de código mais repetido em projetos de dados.
# Se o JSON for uma lista de objetos com as mesmas chaves, o Pandas monta
# a tabela sozinho: cada objeto vira uma linha, cada chave vira coluna.

print("\n--- 5.2 · JSON → DataFrame ---")

dados = resposta.json()
df = pd.DataFrame(dados)
print(df)
print("\npreço médio:", df["preco"].mean())


# ──────────────────────────────────────────────────────────────────────
# 5.3 · Parâmetros: filtrando a consulta
# ──────────────────────────────────────────────────────────────────────
# Você escreve um DICIONÁRIO, não a URL. O requests monta a query string,
# codifica os caracteres especiais e evita erro de digitação e de acento.

print("\n--- 5.3 · params ---")

parametros = {"categoria": "Informática"}
resposta = requests.get(f"{URL_BASE}/produtos", params=parametros, timeout=10)

print("URL montada :", resposta.url)     # repare no acento codificado
print(pd.DataFrame(resposta.json())[["produto", "categoria", "preco"]])


# ──────────────────────────────────────────────────────────────────────
# 5.4 · Headers e autenticação — a regra que não se negocia
# ──────────────────────────────────────────────────────────────────────
# NUNCA escreva tokens no código. Um token comitado é um vazamento de
# credencial, mesmo em repositório privado.
#
#   variável de ambiente   os.getenv("API_TOKEN")
#   arquivo .env fora do Git   python-dotenv + .gitignore
#   gerenciador de segredo     Vault, AWS Secrets Manager

print("\n--- 5.4 · headers e autenticação ---")

token = os.getenv("API_TOKEN", "")
cabecalhos = {"Authorization": f"Bearer {token}"} if token else {}

if token:
    print("enviando Authorization: Bearer ***  (lido de os.getenv)")
else:
    print("API_TOKEN não está no ambiente — nossa API local não exige token.")
    print("Numa API real seria assim:")
    print('  cabecalhos = {"Authorization": f"Bearer {os.getenv(\'API_TOKEN\')}"}')

resposta = requests.get(f"{URL_BASE}/produtos", headers=cabecalhos, timeout=10)
print("status:", resposta.status_code)


# ──────────────────────────────────────────────────────────────────────
# 5.5 · Status HTTP, ao vivo
# ──────────────────────────────────────────────────────────────────────
# A nossa própria API responde os erros do módulo 04 — dá para ver os
# números acontecendo de verdade.

print("\n--- 5.5 · status ao vivo ---")

for caminho, esperado in [
    ("/produtos/1", "200 · existe"),
    ("/produtos/999", "404 · não existe (regra de negócio, escrita à mão)"),
    ("/produtos/abc", "422 · 'abc' não é um int (validação automática)"),
    ("/rota-que-nao-existe", "404 · nem a rota existe"),
]:
    r = requests.get(f"{URL_BASE}{caminho}", timeout=10)
    print(f"  {r.status_code}  GET {caminho:<24} {esperado}")


# ──────────────────────────────────────────────────────────────────────
# 5.6 · Tratamento de erros: três níveis
# ──────────────────────────────────────────────────────────────────────
# Toda requisição pode falhar: a rede cai, o token expira, o servidor sai
# do ar. Os três níveis, do mais ingênuo ao de produção.

print("\n--- 5.6 · tratamento de erros ---")

url_ruim = f"{URL_BASE}/produtos/999"

# NÍVEL 1 · verificar o status na mão
resposta = requests.get(url_ruim, timeout=10)
if resposta.status_code == 200:
    dados = resposta.json()
else:
    print("  nível 1 — Erro:", resposta.status_code)

# NÍVEL 2 · deixar o requests avisar
try:
    resposta = requests.get(url_ruim, timeout=10)
    resposta.raise_for_status()          # converte 4xx e 5xx em exceção
except requests.exceptions.HTTPError as erro:
    print("  nível 2 —", erro)

# NÍVEL 3 · versão de produção
# timeout          evita travar o script para sempre
# raise_for_status converte 4xx e 5xx em exceção
# RequestException cobre rede, DNS e timeout — é a exceção-mãe
try:
    resposta = requests.get(url_ruim, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
except requests.exceptions.RequestException as erro:
    print("  nível 3 — Erro ao acessar API:", type(erro).__name__)


# ──────────────────────────────────────────────────────────────────────
# 5.7 · O pipeline de consumo, do início ao fim
# ──────────────────────────────────────────────────────────────────────
#   OBTER      API → requests → JSON
#   PREPARAR   Pandas → limpeza → NumPy
#   ENTENDER   análise → Matplotlib/Seaborn → insight

print("\n--- 5.7 · o pipeline completo ---")

resposta = requests.get(f"{URL_BASE}/produtos", timeout=10)
resposta.raise_for_status()

df = pd.DataFrame(resposta.json())
df["faturamento"] = df["preco"] * df["vendas"]

print(df[["produto", "preco", "vendas", "faturamento"]])
print("\npreço médio        : R$", round(df["preco"].mean(), 2))
print("produto mais caro  :", df.loc[df["preco"].idxmax(), "produto"])
print("quem mais fatura   :", df.loc[df["faturamento"].idxmax(), "produto"])

print("\n" + "=" * 66)
print("Resumo: requests é a porta de ENTRADA dos dados. No módulo 06")
print("invertemos o papel e escrevemos a porta de SAÍDA.")
print("Próximo: main.py (a API) e lab/07_exercicio.py")
print("=" * 66)
