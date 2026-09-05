"""
SentimentAPI — demo de FastAPI para a aula da PUC.

Uma API que analisa o sentimento de avaliações de filmes em português.
O modelo de "IA" é um classificador baseado em léxico, escrito em Python
puro — para que qualquer iniciante consiga ler TODAS as linhas.

Como rodar (na pasta deste arquivo):

    pip install fastapi uvicorn
    uvicorn main:app --reload

Depois abra no navegador:

    http://127.0.0.1:8000       -> a API
    http://127.0.0.1:8000/docs  -> documentação interativa (Swagger UI)
    http://127.0.0.1:8000/redoc -> documentação alternativa (ReDoc)

Repare: esta docstring que você está lendo aparece na página /docs.
É o primeiro exemplo do poder do FastAPI — a documentação se escreve sozinha
a partir do seu código.
"""

# ──────────────────────────────────────────────────────────────────────
# 1. IMPORTS E O "CÉREBRO" DA APLICAÇÃO (a nossa mini-IA)
# ──────────────────────────────────────────────────────────────────────

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# Um classificador de sentimentos por léxico: cada palavra conhecida tem um
# peso. Somamos os pesos do texto e decidimos o sentimento pela pontuação.
# Nada de scikit-learn — o objetivo é que um iniciante entenda 100% da "IA".
LEXICO: dict[str, int] = {
    # positivas
    "ótimo": 2, "otimo": 2, "excelente": 3, "adoro": 3, "adorei": 3,
    "amei": 3, "maravilhoso": 3, "incrível": 2, "incrivel": 2,
    "divertido": 1, "recomendo": 2, "emocionante": 2, "lindo": 2,
    "perfeito": 3, "obrigado": 1, "melhor": 1, "genial": 2, "top": 1,
    # negativas
    "horrível": -3, "horrivel": -3, "péssimo": -3, "pessimo": -3,
    "odiei": -3, "odeio": -3, "chato": -2, "cansativo": -2,
    "perdi": -1, "tempo": -1, "clichê": -1, "cliche": -1,
    "ruim": -2, "pior": -2, "lamentável": -3, "lamentavel": -3,
    "decepcionante": -2, "não": -1, "nao": -1,
}


def classificar(texto: str) -> dict:
    """Roda o 'modelo': tokeniza, soma os pesos do léxico e devolve o veredito."""
    palavras = texto.lower().replace("!", " ").replace(",", " ").split()
    encontradas = [
        (p, LEXICO[p]) for p in palavras if p in LEXICO
    ]
    pontuacao = sum(peso for _, peso in encontradas)

    if pontuacao > 0:
        sentimento = "positivo"
    elif pontuacao < 0:
        sentimento = "negativo"
    else:
        sentimento = "neutro"

    total = sum(abs(peso) for _, peso in encontradas)
    confianca = min(0.99, 0.5 + 0.1 * total)  # cresce com cada palavra reconhecida

    return {
        "sentimento": sentimento,
        "pontuacao": pontuacao,
        "confianca": round(confianca, 2),
        "palavras_encontradas": encontradas,
    }


# ──────────────────────────────────────────────────────────────────────
# 2. MODELOS PYDANTIC — classes que definem o CONTRATO da API
# ──────────────────────────────────────────────────────────────────────


class AvaliacaoEntrada(BaseModel):
    """O que o cliente ENVIA ao criar uma avaliação.

    Cada anotação (Field, description, ge, le) vira validação automática
    E documentação automática. Envie nota=42 e a API responde 422 sozinha.
    """

    texto: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="O texto da avaliação do filme",
        examples=["Adorei o filme, emocionante do início ao fim!"],
    )
    nota: int = Field(
        ...,
        ge=1,
        le=5,
        description="Nota de 1 a 5 estrelas",
        examples=[5],
    )
    autor: str | None = Field(
        default=None,
        max_length=60,
        description="Quem escreveu (opcional)",
        examples=["Maria"],
    )


class AvaliacaoResposta(AvaliacaoEntrada):
    """O que a API DEVOLVE: a avaliação + o resultado da análise de sentimento."""

    id: int = Field(..., description="Identificador único da avaliação")
    criada_em: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Momento do cadastro (UTC)",
    )
    sentimento: str = Field(..., description="positivo | negativo | neutro")
    confianca: float = Field(..., ge=0, le=1, description="Confiança do modelo")


# ──────────────────────────────────────────────────────────────────────
# 3. ESTADO EM MEMÓRIA — o nosso "banco de dados" de brinquedo
# ──────────────────────────────────────────────────────────────────────

BD_AVALIACOES: dict[int, dict] = {}
proximo_id = 1


# ──────────────────────────────────────────────────────────────────────
# 4. A APLICAÇÃO FASTAPI
# ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="SentimentAPI 🎬",
    description="""
Mini-API de exemplo para a aula: avaliações de filmes com análise de
sentimento. Serve para ver, ao vivo, como o FastAPI transforma **type
hints, classes e docstrings** em validação e documentação automáticas.

## O que experimentar
1. **GET /ola/PUC** — o hello world com parâmetro de rota.
2. **POST /avaliacoes** — crie uma avaliação e veja a IA classificar.
3. Tente enviar **nota = 42** ou **texto vazio** e veja o erro 422.
4. **GET /docs** já está aberto — você está lendo isto aqui dentro.
""",
    version="1.0.0",
)


# ── 4.1 Hello world ───────────────────────────────────────────────────


@app.get("/", tags=["Básico"])
def raiz() -> dict:
    """O hello world. Um dicionário vira JSON automaticamente."""
    return {"mensagem": "Olá! Bem-vindo à SentimentAPI. Abra /docs"}


@app.get("/ola/{nome}", tags=["Básico"], summary="Cumprimenta alguém")
def ola(nome: str) -> dict:
    """Recebe um **parâmetro de rota**.

    Experimente `/ola/PUC` — depois experimente `/ola/` (roda 404) e
    repare: é o type hint `nome: str` que diz ao FastAPI o que esperar.
    """
    return {"mensagem": f"Olá, {nome}! 👋"}


# ── 4.2 Dados: guardar e listar avaliações ────────────────────────────


@app.post(
    "/avaliacoes",
    response_model=AvaliacaoResposta,
    status_code=201,
    tags=["Avaliações"],
    summary="Cadastra uma avaliação e roda a IA",
)
def criar_avaliacao(avaliacao: AvaliacaoEntrada) -> AvaliacaoResposta:
    """Recebe o corpo JSON já **validado** pelo Pydantic, roda o
    classificador de sentimentos e guarda o resultado.

    - `avaliacao: AvaliacaoEntrada` no parâmetro ⇒ o FastAPI lê o JSON do
      corpo da requisição e valida campo a campo.
    - `response_model=AvaliacaoResposta` ⇒ a resposta também tem contrato,
      e aparece modelada na documentação.
    """
    global proximo_id
    resultado = classificar(avaliacao.texto)

    registro = AvaliacaoResposta(
        id=proximo_id,
        **avaliacao.model_dump(),
        sentimento=resultado["sentimento"],
        confianca=resultado["confianca"],
    )
    BD_AVALIACOES[proximo_id] = registro.model_dump()
    proximo_id += 1
    return registro


@app.get("/avaliacoes", response_model=list[AvaliacaoResposta], tags=["Avaliações"])
def listar_avaliacoes(
    sentimento: str | None = None,
    nota_minima: int | None = Query(default=None, ge=1, le=5),
) -> list[AvaliacaoResposta]:
    """Lista avaliações com **filtros por query string** (opcionais).

    Query string é o que vem depois do `?` na URL. Experimente:

        /avaliacoes?sentimento=positivo
        /avaliacoes?nota_minima=4
        /avaliacoes?nota_minima=99   <- e veja o 422 do Query(ge=1, le=5)

    Detalhe fino: no corpo da requisição usamos `Field` (Pydantic); em query
    string usamos `Query` — mesma ideia, lugares diferentes.
    """
    resultados = list(BD_AVALIACOES.values())
    if sentimento is not None:
        resultados = [a for a in resultados if a["sentimento"] == sentimento]
    if nota_minima is not None:
        resultados = [a for a in resultados if a["nota"] >= nota_minima]
    return [AvaliacaoResposta(**a) for a in resultados]  # type: ignore[arg-type]


@app.get("/avaliacoes/{id_avaliacao}", response_model=AvaliacaoResposta, tags=["Avaliações"])
def buscar_avaliacao(id_avaliacao: int) -> AvaliacaoResposta:
    """Busca uma avaliação pelo id.

    Dois aprendizados aqui:
    1. `id_avaliacao: int` ⇒ `/avaliacoes/abc` responde 422 na hora.
    2. Não achou? Nós mesmos levantamos o 404 com `HTTPException`.
    """
    if id_avaliacao not in BD_AVALIACOES:
        raise HTTPException(
            status_code=404,
            detail=f"Avaliação {id_avaliacao} não existe. Cadastre em POST /avaliacoes.",
        )
    return AvaliacaoResposta(**BD_AVALIACOES[id_avaliacao])  # type: ignore[arg-type]


# ── 4.3 A IA exposta diretamente ──────────────────────────────────────


@app.get("/predizer", tags=["IA"], summary="Classifica um texto na hora")
def predizer_get(
    texto: str = Query(min_length=3, description="Texto para analisar"),
) -> dict:
    """Atalho para testar o classificador sem corpo JSON — só query string:

        /predizer?texto=Filme maravilhoso, adorei demais
    """
    return classificar(texto)


@app.post("/predizer", tags=["IA"], summary="Classifica via corpo JSON")
def predizer_post(payload: dict) -> dict:
    """Mesma IA, agora recebendo um JSON `{"texto": "..."}` no corpo.

    Um `dict` cru funciona, mas compare com `AvaliacaoEntrada`:
    sem Pydantic não há validação, nem exemplos, nem modelo na documentação.
    É a diferença entre uma API que se documenta e uma que se explica.
    """
    if "texto" not in payload:
        raise HTTPException(status_code=422, detail="Envie {'texto': '...'}")
    return classificar(payload["texto"])


# ── 4.4 Estatísticas — fechando a parte de "dados" ────────────────────


@app.get("/estatisticas", tags=["Dados"])
def estatisticas() -> dict:
    """Painelzinho de dados: contagem por sentimento e nota média."""
    avaliacoes = list(BD_AVALIACOES.values())
    if not avaliacoes:
        return {"total": 0, "dica": "Cadastre avaliações em POST /avaliacoes"}

    por_sentimento: dict[str, int] = {}
    for a in avaliacoes:
        por_sentimento[a["sentimento"]] = por_sentimento.get(a["sentimento"], 0) + 1

    media_nota = sum(a["nota"] for a in avaliacoes) / len(avaliacoes)
    return {
        "total": len(avaliacoes),
        "por_sentimento": por_sentimento,
        "nota_media": round(media_nota, 2),
    }
