"""
ProdutosAPI — a stack inteira, servida por uma API
==================================================

**Esta é a nossa parte da aula: FastAPI.**

Os módulos anteriores (NumPy, Pandas, Matplotlib/Seaborn, APIs, requests)
não ficam para trás — eles entram AQUI. Cada camada da pilha vira um
endpoint, e é assim que este arquivo ensina FastAPI: mostrando que o
framework é onde o trabalho de dados **encontra o mundo**.

    NumPy      →  /numpy/vetorizacao   ·  /numpy/estatisticas
    Pandas     →  /produtos            ·  /produtos/por-categoria
    Matplotlib →  /produtos/grafico
    Análise    →  /produtos/media      ·  /estatisticas

Uma análise que vive só no notebook não é usada por ninguém. Publicada
aqui, ela vira insumo para um site, um painel, um aplicativo ou outro
time — inclusive as previsões de um modelo de Machine Learning.

Como rodar (na pasta deste arquivo):

    uv run uvicorn main:app --reload

Depois abra no navegador:

    http://127.0.0.1:8000        -> a API
    http://127.0.0.1:8000/docs   -> documentação interativa (Swagger UI)
    http://127.0.0.1:8000/redoc  -> documentação alternativa (ReDoc)

Repare: esta docstring que você está lendo aparece na página /docs.
É o primeiro exemplo do poder do FastAPI — a documentação se escreve
sozinha a partir do seu código.
"""

# ──────────────────────────────────────────────────────────────────────
# 1. IMPORTS E OS DADOS
# ──────────────────────────────────────────────────────────────────────

import io
from pathlib import Path

import matplotlib

# Num servidor web não há tela para desenhar. "Agg" é o motor que desenha
# direto na memória — e precisa ser escolhido ANTES de importar o resto.
matplotlib.use("Agg")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from fastapi import FastAPI, HTTPException, Query, Response  # noqa: E402
from matplotlib.backends.backend_agg import FigureCanvasAgg  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

# O mesmo CSV que o módulo 02 leu. O dado percorre a pilha inteira.
DADOS = Path(__file__).parent / "lab" / "dados" / "produtos.csv"


# ──────────────────────────────────────────────────────────────────────
# 2. MODELOS PYDANTIC — classes que definem o CONTRATO da API
# ──────────────────────────────────────────────────────────────────────


class ProdutoEntrada(BaseModel):
    """O que o cliente ENVIA ao cadastrar um produto.

    Cada anotação (Field, description, ge, min_length) vira validação
    automática E documentação automática. Envie preco = -5 e a API
    responde 422 sozinha — sem você escrever um único `if`.
    """

    produto: str = Field(
        ...,
        min_length=2,
        max_length=60,
        description="Nome do produto",
        examples=["Teclado"],
    )
    categoria: str = Field(
        ...,
        min_length=2,
        max_length=40,
        description="Categoria do produto",
        examples=["Acessórios"],
    )
    preco: float = Field(
        ...,
        gt=0,
        le=1_000_000,
        description="Preço em reais (maior que zero)",
        examples=[90.0],
    )
    vendas: int = Field(
        default=0,
        ge=0,
        description="Unidades vendidas",
        examples=[210],
    )


class ProdutoResposta(ProdutoEntrada):
    """O que a API DEVOLVE: o produto cadastrado + o que ela calculou."""

    id: int = Field(..., description="Identificador único do produto")
    faturamento: float = Field(..., description="preco × vendas, calculado pela API")


class Estatisticas(BaseModel):
    """O resumo do catálogo — o resultado de uma análise, virando resposta."""

    total_produtos: int
    preco_medio: float
    preco_mediano: float
    preco_desvio_padrao: float
    produto_mais_caro: str
    faturamento_total: float
    por_categoria: dict[str, float]


# ──────────────────────────────────────────────────────────────────────
# 3. ESTADO — o nosso "banco de dados" de brinquedo
# ──────────────────────────────────────────────────────────────────────
# Um DataFrame em memória, carregado do CSV. Não escala, e não é para
# escalar: é didático. Trocar isto por SQLite ou Postgres muda umas
# poucas linhas — e nenhuma das rotas abaixo.

catalogo: pd.DataFrame = pd.read_csv(DADOS)
catalogo.insert(0, "id", range(1, len(catalogo) + 1))


def _para_dicionarios(df: pd.DataFrame) -> list[dict]:
    """Converte um DataFrame em lista de dicionários, já com faturamento."""
    saida = df.copy()
    saida["faturamento"] = saida["preco"] * saida["vendas"]
    return saida.to_dict(orient="records")


# ──────────────────────────────────────────────────────────────────────
# 4. A APLICAÇÃO FASTAPI
# ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="ProdutosAPI 🛒",
    description="""
**A stack inteira da aula, servida por endpoints.** O mesmo dado que entrou
por um arquivo, virou tabela no Pandas, virou número no NumPy e virou
gráfico no Matplotlib — aqui ele volta a ser API, disponível para qualquer
sistema que saiba fazer uma requisição HTTP.

Cada seção abaixo é uma camada da pilha virando endpoint:

| Camada | Endpoints |
|---|---|
| **NumPy** | `/numpy/vetorizacao` · `/numpy/estatisticas` |
| **Pandas** | `/produtos` · `/produtos/por-categoria` |
| **Matplotlib** | `/produtos/grafico` |
| **Análise** | `/produtos/media` · `/estatisticas` |

## O que experimentar
1. **GET /numpy/vetorizacao?valores=10,20,30** — a vetorização, por HTTP.
2. **GET /produtos** — o catálogo (é este JSON que o `requests` consome).
3. **GET /produtos/por-categoria** — o `groupby` do Pandas, servido.
4. **GET /produtos/media** — o resultado da análise, servido como API.
5. **POST /produtos** — cadastre um produto e veja o Pydantic validar.
6. Tente enviar **preco = -5** e veja o erro **422** aparecer sozinho.
7. **GET /produtos/grafico** — um gráfico Matplotlib entregue por HTTP.
""",
    version="2.0.0",
)


# ── 4.1 Hello world ───────────────────────────────────────────────────


@app.get("/", tags=["Básico"])
def inicio() -> dict:
    """O hello world. Um dicionário Python vira JSON automaticamente."""
    return {"mensagem": "Minha primeira API", "documentacao": "/docs"}


@app.get("/ola/{nome}", tags=["Básico"], summary="Cumprimenta alguém")
def ola(nome: str) -> dict:
    """Recebe um **parâmetro de caminho** — o pedaço variável da URL.

    Experimente `/ola/PUC`. É o type hint `nome: str` que diz ao FastAPI
    o que esperar ali.
    """
    return {"mensagem": f"Olá, {nome}! 👋"}


# ── 4.2 NUMPY SERVIDO — a camada de cálculo virando endpoint ──────────
# O módulo 01 rodou no terminal. As MESMAS operações, agora acessíveis por
# HTTP: é a primeira vez que a pilha encontra o mundo de fora.


@app.get("/numpy/vetorizacao", tags=["NumPy"], summary="A vetorização, por HTTP")
def numpy_vetorizacao(
    valores: str = Query(
        default="10,20,30",
        description="Números separados por vírgula",
        examples=["10,20,30"],
    ),
    operacao: str = Query(
        default="dobrar",
        pattern="^(dobrar|somar5|quadrado|maiores_que_15)$",
        description="dobrar | somar5 | quadrado | maiores_que_15",
    ),
) -> dict:
    """A operação que vale para o array inteiro — agora como serviço.

    Experimente `/numpy/vetorizacao?valores=10,20,30&operacao=dobrar`.

    Repare no `pattern=` do Query: só quatro operações são aceitas, e quem
    mandar outra recebe **422** — a validação está no CONTRATO, não num
    `if` escondido dentro da função.
    """
    # Dois 422 no mesmo endpoint, e vale comparar em aula:
    #   `operacao` inválida  -> 422 AUTOMÁTICO, veio do pattern= do Query
    #   `valores` inválido   -> 422 MANUAL, porque "lista de números numa
    #                           string" não é um tipo que o Python conheça
    # Sempre que der para expressar a regra no CONTRATO, prefira o de cima.
    try:
        array = np.array([float(v) for v in valores.split(",") if v.strip()])
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"'{valores}' não é uma lista de números separados por vírgula.",
        ) from None

    if array.size == 0:
        raise HTTPException(status_code=422, detail="Envie ao menos um número.")

    # Sem laço, sem índice: a operação se propaga elemento a elemento.
    resultados = {
        "dobrar": array * 2,
        "somar5": array + 5,
        "quadrado": array**2,
        "maiores_que_15": array > 15,
    }
    resultado = resultados[operacao]

    return {
        "entrada": array.tolist(),
        "operacao": operacao,
        "resultado": resultado.tolist(),
        "como_seria_sem_numpy": "resultado = []; for v in valores: resultado.append(...)",
        "observacao": "Uma linha, sem laço. A repetição acontece em código compilado.",
    }


@app.get("/numpy/estatisticas", tags=["NumPy"], summary="Estatística em uma linha")
def numpy_estatisticas(
    valores: str = Query(
        default="7.5,8.0,6.5,9.0,8.5",
        description="Números separados por vírgula",
    ),
) -> dict:
    """As estatísticas do módulo 01 (`mean`, `max`, `std`…) como serviço.

    Note o `float()` em cada valor: o NumPy devolve `np.float64` e o JSON
    quer um número do Python. É o detalhe que só aparece quando se PUBLICA.
    """
    try:
        array = np.array([float(v) for v in valores.split(",") if v.strip()])
    except ValueError:
        raise HTTPException(
            status_code=422, detail=f"'{valores}' não é uma lista de números."
        ) from None

    if array.size == 0:
        raise HTTPException(status_code=422, detail="Envie ao menos um número.")

    return {
        "valores": array.tolist(),
        "media": float(array.mean()),
        "maximo": float(array.max()),
        "minimo": float(array.min()),
        "desvio_padrao": float(array.std()),
        "mediana": float(np.median(array)),
        "posicao_do_maior": int(array.argmax()),
    }


# ── 4.3 PANDAS SERVIDO — a tabela virando endpoint ────────────────────
# O catálogo que o módulo 02 leu com pd.read_csv() é o mesmo que sai
# aqui em JSON. Filtros de query string são máscaras booleanas do Pandas.


@app.get("/produtos", response_model=list[ProdutoResposta], tags=["Produtos"])
def listar_produtos(
    categoria: str | None = Query(default=None, description="Filtra por categoria"),
    preco_maximo: float | None = Query(default=None, gt=0, description="Preço teto"),
) -> list[dict]:
    """Lista o catálogo, com **filtros opcionais por query string**.

    Query string é o que vem depois do `?` na URL. Experimente:

        /produtos?categoria=Informática
        /produtos?preco_maximo=1500
        /produtos?preco_maximo=-1   <- e veja o 422 do Query(gt=0)

    Detalhe fino que confunde todo mundo no começo: no CORPO da
    requisição usamos `Field` (Pydantic); na URL usamos `Query`.
    Mnemônico: **Field no corpo, Query na URL**.
    """
    filtrado = catalogo
    # Cada filtro é uma máscara booleana — a mesma ideia do módulo 01.
    if categoria is not None:
        filtrado = filtrado[filtrado["categoria"] == categoria]
    if preco_maximo is not None:
        filtrado = filtrado[filtrado["preco"] <= preco_maximo]
    return _para_dicionarios(filtrado)


@app.post(
    "/produtos",
    response_model=ProdutoResposta,
    status_code=201,
    tags=["Produtos"],
    summary="Cadastra um produto",
)
def criar_produto(produto: ProdutoEntrada) -> dict:
    """Recebe o corpo JSON já **validado** pelo Pydantic e o acrescenta
    ao catálogo.

    - `produto: ProdutoEntrada` no parâmetro ⇒ o FastAPI lê o JSON do
      corpo da requisição e confere campo a campo.
    - `status_code=201` ⇒ o status correto para "criei o recurso"
      (o 200 significa apenas "deu certo").
    - `response_model=ProdutoResposta` ⇒ a resposta também tem contrato,
      e aparece modelada na documentação.
    """
    global catalogo

    novo_id = int(catalogo["id"].max()) + 1 if len(catalogo) else 1
    linha = {"id": novo_id, **produto.model_dump()}
    catalogo = pd.concat([catalogo, pd.DataFrame([linha])], ignore_index=True)
    return _para_dicionarios(catalogo[catalogo["id"] == novo_id])[0]


# ── 4.4 ANÁLISE E VISUALIZAÇÃO SERVIDAS ───────────────────────────────
# É aqui que a aula fecha: o resultado de uma análise — e até o gráfico —
# entregues por HTTP. É assim que modelos de ML chegam à produção.


@app.get(
    "/produtos/por-categoria",
    tags=["Pandas"],
    summary="O groupby do Pandas, servido",
)
def produtos_por_categoria() -> dict:
    """O `split · apply · combine` do módulo 02, agora como endpoint.

    A mesma linha do slide de agrupamento:

        catalogo.groupby("categoria")["preco"].sum()

    Cadastre o Teclado em `POST /produtos` e volte aqui: o resultado passa
    a ser **Acessórios 240 / Informática 5700** — os números do slide,
    calculados ao vivo.
    """
    agrupado = catalogo.groupby("categoria").agg(
        itens=("produto", "count"),
        preco_total=("preco", "sum"),
        preco_medio=("preco", "mean"),
    )
    return {
        str(categoria): {
            "itens": int(linha["itens"]),
            "preco_total": float(linha["preco_total"]),
            "preco_medio": round(float(linha["preco_medio"]), 2),
        }
        for categoria, linha in agrupado.iterrows()
    }


@app.get("/produtos/media", tags=["Análise"], summary="O preço médio do catálogo")
def preco_medio() -> dict:
    """O resultado da análise, **servido como API** — o exercício da aula.

    Uma média calculada no notebook morre no notebook. Publicada aqui,
    ela vira insumo para um site, um painel ou outro sistema.
    """
    media = catalogo["preco"].mean()
    return {"preco_medio": float(media)}


@app.get("/estatisticas", response_model=Estatisticas, tags=["Análise"])
def estatisticas() -> dict:
    """O painel do catálogo: Pandas e NumPy trabalhando **dentro** de um
    endpoint.

    É este o desenho que leva um modelo de Machine Learning à produção:

        cliente → FastAPI → Pandas / NumPy / modelo → resultado → JSON
    """
    precos = catalogo["preco"].to_numpy()
    faturamento = catalogo["preco"] * catalogo["vendas"]

    return {
        "total_produtos": len(catalogo),
        # float() porque o NumPy devolve np.float64, e o JSON quer número
        # do Python. É o tipo de detalhe que só aparece quando se publica.
        "preco_medio": float(precos.mean()),
        "preco_mediano": float(np.median(precos)),
        "preco_desvio_padrao": float(precos.std()),
        "produto_mais_caro": str(catalogo.loc[catalogo["preco"].idxmax(), "produto"]),
        "faturamento_total": float(faturamento.sum()),
        "por_categoria": {
            str(categoria): float(total)
            for categoria, total in catalogo.groupby("categoria")["preco"].sum().items()
        },
    }


@app.get(
    "/produtos/grafico",
    tags=["Análise"],
    summary="O gráfico de barras, entregue por HTTP",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}, "description": "PNG do gráfico"}},
)
def grafico() -> Response:
    """Uma API não devolve só JSON. Aqui ela devolve uma **imagem PNG**
    desenhada na hora pelo Matplotlib.

    Abra `/produtos/grafico` direto no navegador.

    Nota técnica: num servidor usamos a API de objetos do Matplotlib
    (`Figure`), e não o `pyplot` global — o `pyplot` guarda estado
    compartilhado, o que dá problema quando vários pedidos chegam juntos.
    """
    figura = Figure(figsize=(8, 4.5))
    FigureCanvasAgg(figura)
    eixo = figura.subplots()

    eixo.bar(catalogo["produto"], catalogo["preco"], color="#2dd4bf")
    eixo.set_title("Preço por Produto")
    eixo.set_xlabel("Produto")
    eixo.set_ylabel("Preço (R$)")
    figura.tight_layout()

    buffer = io.BytesIO()
    figura.savefig(buffer, format="png", dpi=110)
    return Response(content=buffer.getvalue(), media_type="image/png")


# ── 4.5 A ORDEM DAS ROTAS IMPORTA ─────────────────────────────────────
# Esta rota fica por ÚLTIMO de propósito, e é a lição mais fácil de
# esquecer: o FastAPI testa as rotas de cima para baixo e para na
# primeira que casa. `/produtos/{produto_id}` casa com QUALQUER coisa
# depois de /produtos/ — inclusive com "media" e com "grafico".
#
# Se ela viesse antes, `/produtos/media` tentaria converter "media" em
# int e responderia 422. Regra prática: **rotas com caminho fixo vêm
# antes das rotas com parâmetro**.


@app.get(
    "/produtos/{produto_id}",
    response_model=ProdutoResposta,
    tags=["Produtos"],
)
def buscar_produto(produto_id: int) -> dict:
    """Busca um produto pelo id.

    Dois aprendizados de uma vez:

    1. `produto_id: int` ⇒ `/produtos/abc` responde **422** na hora, com
       uma mensagem clara, sem você escrever validação nenhuma.
    2. Não achou? O **404 é nosso**, escrito à mão com `HTTPException`.

    A diferença é sutil e importante: **422 = pedido malformado**
    (automático); **404 = regra de negócio** (manual).
    """
    encontrado = catalogo[catalogo["id"] == produto_id]
    if encontrado.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Produto {produto_id} não existe. Veja a lista em GET /produtos.",
        )
    return _para_dicionarios(encontrado)[0]
