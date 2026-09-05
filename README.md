# A Stack Base de Ciência de Dados com Python

Material executável da aula **"A Stack Base de Ciência de Dados com Python"** —
NumPy · Pandas · Matplotlib · Seaborn · APIs · requests · FastAPI.

Plano de aula do prof. **Leonardo Afonso Amorim**, que cobre os módulos
01–05 (NumPy, Pandas, Matplotlib/Seaborn, APIs e requests).
**A nossa parte é o módulo 06: FastAPI** — e é o que este repositório entrega,
com todo o resto integrado nele.

Por isso o FastAPI aqui não é o último assunto de uma lista: é a **espinha**.
Cada camada da pilha roda no terminal **e** tem um endereço na API, e é ao
ligar os dois que o framework é ensinado.

```
NumPy       →  GET /numpy/vetorizacao   ·  GET /numpy/estatisticas
Pandas      →  GET /produtos            ·  GET /produtos/por-categoria
Matplotlib  →  GET /produtos/grafico
APIs        →  GET /openapi.json        ·  /docs
Análise     →  GET /produtos/media      ·  GET /estatisticas
```

> **A tese:** *Ciência de Dados não termina no DataFrame.* Dados precisam ser
> obtidos, processados, analisados, visualizados e — com frequência —
> **disponibilizados** para outros sistemas.

## Rodar

Este projeto usa **[uv](https://docs.astral.sh/uv/)** — o gerenciador de
pacotes e ambientes do Python. Se você nunca usou, são dois comandos até a
API no ar.

### 1. Instalar o uv (uma vez na vida)

```bash
# Linux e macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Feche e reabra o terminal, e confira: `uv --version`.

> Também dá para instalar com `pipx install uv`, `brew install uv` ou
> `pip install uv` — tanto faz, é o mesmo programa.

### 2. Clonar e rodar

```bash
git clone https://github.com/m-da-costa/presentation_fast_api.git
cd presentation_fast_api

uv run uvicorn main:app --reload      # → http://127.0.0.1:8000/docs
```

**É só isso.** Você não precisa criar `venv`, nem ativar nada, nem instalar
dependência nenhuma: na primeira vez que você roda `uv run`, o uv baixa a
versão certa do Python, cria o ambiente em `.venv/` e instala tudo o que
está no `pyproject.toml`. Depois disso ele só confere e executa — em
milissegundos.

### Os três comandos que você vai usar

| Comando | O que faz |
|---|---|
| `uv run <arquivo.py>` | roda um script **no ambiente do projeto** (sincroniza antes, se precisar) |
| `uv sync` | instala/atualiza o ambiente sem rodar nada — útil antes da aula, com Wi-Fi bom |
| `uv add <pacote>` | acrescenta uma dependência ao `pyproject.toml` e ao `uv.lock` |

Nada de `pip install` solto e nada de `source .venv/bin/activate`: o prefixo
`uv run` já coloca você dentro do ambiente certo.

### Quem controla as versões

- **`pyproject.toml`** — as dependências que nós pedimos, com versões mínimas.
- **`uv.lock`** — as versões exatas que foram resolvidas. É ele que garante
  que a sua máquina e a do professor rodem **o mesmo código**. Está versionado
  no Git de propósito; não edite à mão.

### Sem uv? (plano B)

Funciona com `pip`, mas você cuida do ambiente na mão:

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

O `requirements.txt` lista as mesmas dependências diretas do
`pyproject.toml`. Nesse caminho, ignore o prefixo `uv run` dos exemplos
abaixo — com o ambiente ativado, `python lab/01_numpy.py` basta.

## Os oito módulos

| # | Módulo | Arquivo | O que ensina | Termina em |
|---|---|---|---|---|
| 01 | NumPy | `lab/01_numpy.py` | ndarray, vetorização, máscara booleana, estatística, e a medição real lista × array | `/numpy/estatisticas` |
| 02 | Pandas | `lab/02_pandas.py` | Series/DataFrame, filtro, `describe()`, `groupby` (split·apply·combine), ponte para o NumPy | `/produtos/por-categoria` |
| 03 | Visualização | `lab/03_visualizacao.py` | Matplotlib camada a camada, os 4 gráficos, Seaborn com `data=df`, boxplot e scatterplot | `/produtos/grafico` |
| 04 | APIs | `lab/04_json_xml.py` | JSON × XML na prática, métodos HTTP, status, autenticação | `/openapi.json` |
| 05 | requests | `lab/05_requests.py` | `status_code`/`.json()`, JSON→DataFrame, `params`, headers, 3 níveis de tratamento de erro | consome tudo acima |
| 06 | **FastAPI** | **`main.py`** | **a nossa parte** — onde as cinco camadas acima viram serviço | — |
| 07 | Exercício | `lab/07_exercicio.py` · `lab/07_solucao.py` | juntar tudo em um script | `/produtos/media` |
| 08 | Quiz | `lab/08_quiz.py` | as 7 perguntas de fechamento, com correção | — |

Os módulos **01–05 são a aula do prof. Leonardo** — ficam aqui para o aluno
rodar em casa. O **06 é a nossa parte**, e é onde os outros desaguam:
**cada módulo termina chamando o endpoint que o serve.** Suba a API antes e
rode os módulos com ela no ar — é aí que a aula fecha. Sem a API no ar todos
os arquivos continuam rodando: eles avisam e seguem sem o último bloco.

```bash
uv run lab/01_numpy.py
uv run lab/02_pandas.py
uv run lab/03_visualizacao.py      # gráficos vão para lab/saida/*.png
uv run lab/04_json_xml.py
uv run lab/05_requests.py          # precisa da API no ar
uv run lab/07_solucao.py
uv run lab/08_quiz.py              # --respostas mostra só o gabarito
```

## O fio condutor

Um único catálogo percorre a aula inteira:

```
lab/dados/produtos.csv  →  Pandas  →  NumPy  →  Matplotlib  →  FastAPI
```

| produto | categoria | preço | vendas |
|---|---|---|---|
| Notebook | Informática | 4500 | 12 |
| Mouse | Acessórios | 150 | 400 |
| Monitor | Informática | 1200 | 40 |

Preço médio **R$ 1.950,00**, produto mais caro **Notebook** — os mesmos números
dos slides, saindo da máquina. (Detalhe que rende discussão: o mais caro é o
Notebook, mas quem mais fatura é o Mouse.)

## A API (`main.py`)

```bash
uv run uvicorn main:app --reload
```

| URL | O que é |
|---|---|
| http://127.0.0.1:8000 | a API |
| http://127.0.0.1:8000/docs | **Swagger UI** interativa (a estrela da demo) |
| http://127.0.0.1:8000/redoc | ReDoc (documentação alternativa) |
| http://127.0.0.1:8000/openapi.json | o contrato OpenAPI gerado |

| Seção | Método | Rota | Ensina o quê |
|---|---|---|---|
| 4.1 | GET | `/` | hello world; dict → JSON |
| 4.1 | GET | `/ola/{nome}` | parâmetro de caminho |
| 4.2 | GET | `/numpy/vetorizacao` | **o módulo 01 servido**; `Query(pattern=)` → 422 automático |
| 4.2 | GET | `/numpy/estatisticas` | `mean`/`std`/`median` por HTTP; o `float()` que o JSON exige |
| 4.3 | GET | `/produtos` | **o módulo 02 servido**; query strings + filtro (`Query(gt=0)`) |
| 4.3 | POST | `/produtos` | corpo JSON + Pydantic + `response_model` + status 201 |
| 4.4 | GET | `/produtos/por-categoria` | o `groupby` do Pandas, publicado |
| 4.4 | GET | `/produtos/media` | o resultado da análise — o exercício da aula |
| 4.4 | GET | `/estatisticas` | Pandas e NumPy **dentro** do endpoint |
| 4.4 | GET | `/produtos/grafico` | **o módulo 03 servido**: um PNG do Matplotlib por HTTP |
| 4.5 | GET | `/produtos/{produto_id}` | conversão de tipo (422) + `HTTPException` (404); **a ordem das rotas** |

## Experimentos que dão certo na demo

1. `GET /numpy/vetorizacao?valores=10,20,30&operacao=dobrar` → a vetorização por HTTP
2. `GET /numpy/vetorizacao?...&operacao=raiz` → **422** vindo do `pattern=` do Query
3. `GET /produtos?categoria=Informática` → filtro por query string
4. `GET /produtos?preco_maximo=-1` → **422 automático** (o `Query(gt=0)`)
5. `POST /produtos` com `preco: -5` → **422 automático** (o `Field(gt=0)`)
6. `GET /produtos/abc` → 422 ("não é int")
7. `GET /produtos/999` → **404** com mensagem amigável (esse é escrito à mão)
8. `POST /produtos` com o Teclado → `/produtos/por-categoria` passa a dar
   **Acessórios 240 / Informática 5700**, os mesmos números que o
   `lab/02_pandas.py` imprimiu no terminal. **É o momento em que a aula fecha.**
9. `GET /produtos/grafico` → o gráfico, no navegador

## Arquivos

- `main.py` — a API, em seções numeradas (1 dados, 2 Pydantic, 3 estado,
  4.1–4.5 os endpoints) para acompanhar a aula.
- `lab/` — um arquivo por módulo, todos comentados em PT-BR.
  - `lab/dados/produtos.csv` — o catálogo que percorre a aula inteira.
  - `lab/saida/` — onde os gráficos são salvos (os PNGs não vão para o Git).
- `AULA.md` — roteiro do instrutor: minuto a minuto, falas e o que fazer quebrar.
- `slides/index.html` — **a apresentação da nossa parte**: 25 slides, do
  hello world ao fecho. É este que se projeta.
- `slides/aula-completa.html` — os 65 slides dos oito módulos, de referência
  (útil se um aluno quiser rever NumPy/Pandas depois). Ambos são
  autocontidos — só o Mermaid e a fonte usam CDN, e degradam sem rede.
- `pyproject.toml` · `uv.lock` — as dependências e as versões exatas.
- `requirements.txt` — as mesmas dependências, para quem for de `pip`.

## Nota sobre o estilo do código

O público-alvo são **alunos iniciantes**, então aqui **clareza vence
elegância**: um `main.py` único em vez de pacotes, nomes em português,
comentários explicando o porquê. Não é o estilo de um serviço de produção —
é de propósito.
