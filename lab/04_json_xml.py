"""
MÓDULO 04 · APIs — JSON x XML, métodos e status HTTP
====================================================

O módulo 04 da aula é sobretudo conceitual (REST x SOAP, anatomia da
requisição, autenticação). Este arquivo é a parte que dá para EXECUTAR:
os mesmos dados nos dois formatos e a tabela de status HTTP.

Rode assim:

    uv run lab/04_json_xml.py
"""

import json
import xml.etree.ElementTree as ET

print("=" * 66)
print("04 · APIs — JSON x XML, métodos e status")
print("=" * 66)


# ──────────────────────────────────────────────────────────────────────
# 4.1 · Os mesmos dados, dois formatos
# ──────────────────────────────────────────────────────────────────────

print("\n--- 4.1 · JSON ---")

texto_json = """
{
  "nome": "Ana",
  "idade": 30
}
"""
pessoa = json.loads(texto_json)     # JSON vira dict do Python, direto
print("texto recebido :", texto_json.strip().replace("\n", " "))
print("virou          :", pessoa, type(pessoa).__name__)
print("acesso         :", pessoa["nome"], pessoa["idade"])

print("\n--- 4.1 · XML ---")

texto_xml = """
<pessoa>
    <nome>Ana</nome>
    <idade>30</idade>
</pessoa>
"""
raiz = ET.fromstring(texto_xml.strip())
print("texto recebido :", texto_xml.strip().replace("\n", " "))
print("virou          :", raiz, type(raiz).__name__)
# Repare no trabalho a mais: procurar cada nó, e tudo volta como TEXTO.
nome = raiz.find("nome").text
idade = int(raiz.find("idade").text)      # a conversão é por sua conta
print("acesso         :", nome, idade)

print(
    "\nPor que JSON domina em APIs REST:\n"
    "  · mais enxuto   — menos caracteres para os mesmos dados\n"
    "  · natural em Python — vira dict e list diretamente\n"
    "  · universal na web  — suporte nativo em qualquer linguagem"
)

# REST x SOAP em uma frase: REST é um ESTILO arquitetural (normalmente
# HTTP + JSON, simples e onipresente nos serviços novos); SOAP é um
# PROTOCOLO formal (XML em envelope, contrato em WSDL) que você vai
# encontrar em integrações bancárias, governamentais e de ERPs.


# ──────────────────────────────────────────────────────────────────────
# 4.2 · Os quatro métodos HTTP essenciais
# ──────────────────────────────────────────────────────────────────────
# O caminho diz O QUÊ; o método diz O QUE FAZER com ele.

print("\n--- 4.2 · Métodos HTTP ---")

METODOS = [
    ("GET", "Consultar dados", "GET    /produtos"),
    ("POST", "Criar / enviar dados", "POST   /produtos"),
    ("PUT", "Atualizar dados", "PUT    /produtos/10"),
    ("DELETE", "Excluir dados", "DELETE /produtos/10"),
]
for metodo, o_que_faz, exemplo in METODOS:
    print(f"  {metodo:<7} {o_que_faz:<22} {exemplo}")

# O MESMO caminho muda de significado conforme o método:
#   GET /produtos/10     consulta o produto 10
#   PUT /produtos/10     atualiza o produto 10
#   DELETE /produtos/10  exclui o produto 10


# ──────────────────────────────────────────────────────────────────────
# 4.3 · Códigos de status HTTP
# ──────────────────────────────────────────────────────────────────────

print("\n--- 4.3 · Status HTTP ---")

STATUS = {
    "2xx · Sucesso": [(200, "OK"), (201, "Created")],
    "4xx · Erro do cliente": [
        (400, "Bad Request"),
        (401, "Unauthorized"),
        (403, "Forbidden"),
        (404, "Not Found"),
        (422, "Unprocessable Entity"),
        (429, "Too Many Requests"),
    ],
    "5xx · Erro do servidor": [
        (500, "Internal Server Error"),
        (503, "Service Unavailable"),
    ],
}
for familia, codigos in STATUS.items():
    print(f"\n  {familia}")
    for codigo, nome in codigos:
        print(f"    {codigo}  {nome}")

print(
    "\n  Os três que mais confundem:\n"
    "    401 = 'não sei quem você é'\n"
    "    403 = 'sei quem você é, mas você não pode'\n"
    "    429 = 'calma, você está pedindo demais'"
)


# ──────────────────────────────────────────────────────────────────────
# 4.4 · Autenticação: quem está pedindo?
# ──────────────────────────────────────────────────────────────────────

print("\n--- 4.4 · Autenticação ---")
print(
    "  API Key       chave fixa em cada requisição   X-API-Key: abc123\n"
    "  Bearer Token  token, normalmente temporário    Authorization: Bearer eyJ...\n"
    "  OAuth         o usuário autoriza a aplicação   'Entrar com o Google'"
)
print(
    "\n  REGRA QUE NÃO SE NEGOCIA: chaves e tokens NUNCA ficam escritos no\n"
    "  código. Um token comitado é um vazamento de credencial — mesmo em\n"
    "  repositório privado. Veja lab/05_requests.py, seção 5.4."
)


# ──────────────────────────────────────────────────────────────────────
# 4.5 · E AGORA PELA API — a nossa API é o exemplo vivo
# ──────────────────────────────────────────────────────────────────────
# Tudo o que está acima é conceito. A nossa API (main.py) é a versão
# concreta: ela FALA esses status, devolve esse JSON e publica o próprio
# contrato — em OpenAPI, o padrão da indústria.
#
#     uv run uvicorn main:app --reload
#
#   http://127.0.0.1:8000/openapi.json   o contrato, em JSON
#   http://127.0.0.1:8000/docs           o contrato, navegável
#
# E o cardápio da analogia do garçom deixa de ser metáfora: é um arquivo.

print("\n--- 4.5 · o contrato da nossa própria API ---")

import os  # noqa: E402

import requests  # noqa: E402

URL_BASE = os.getenv("URL_BASE", "http://127.0.0.1:8000")

try:
    r = requests.get(f"{URL_BASE}/openapi.json", timeout=3)
    r.raise_for_status()
    contrato = r.json()
    print(f"GET {URL_BASE}/openapi.json  ->  {r.status_code}")
    print(f"  título    : {contrato['info']['title']}")
    print(f"  versão    : {contrato['info']['version']}")
    print("  caminhos  :")
    for caminho, metodos in contrato["paths"].items():
        print(f"    {' '.join(m.upper() for m in metodos):<6} {caminho}")
    print("\nNinguém escreveu esse documento. Ele nasceu dos type hints,")
    print("das classes Pydantic e das docstrings do main.py.")
except requests.exceptions.RequestException:
    print("(API fora do ar — suba com `uv run uvicorn main:app --reload`)")


print("\n" + "=" * 66)
print("Resumo: requisição (URL, método, headers, params, body) e resposta")
print("(status, headers, body). Todo o resto da aula é detalhe deste ciclo.")
print("Próximo: lab/05_requests.py")
print("=" * 66)
