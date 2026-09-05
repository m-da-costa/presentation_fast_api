# AULA.md — roteiro do instrutor

**Aula:** A Stack Base de Ciência de Dados com Python
**Plano de aula:** prof. Leonardo Afonso Amorim · **Laboratório:** Ricardo da Costa
**Formato:** exposição + demo ao vivo (o professor programa, os alunos acompanham)
**Público:** iniciantes · **Idioma:** PT-BR

**Tese da aula:** *Ciência de Dados não termina no DataFrame.* O dado é
**obtido**, **processado**, **analisado**, **visualizado** e **disponibilizado** —
e o mesmo catálogo de produtos percorre a pilha inteira, do CSV ao endpoint.

---

## Como este repositório se encaixa no plano

O plano de aula (os 62 slides do professor) tem oito módulos. Este repositório
é a **parte executável** deles — e **a nossa parte da aula é o FastAPI**.

Isso muda o desenho: o FastAPI **não** é o último assunto de uma lista. Ele é
a espinha. Cada módulo anterior roda no terminal **e** tem um endereço na
nossa API, e é ao ligar os dois que o framework é ensinado.

| Módulo do plano | Slides daqui | Roda em | **Servido em** |
|---|---|---|---|
| 01 · NumPy | 7–12 | `lab/01_numpy.py` | `/numpy/vetorizacao` · `/numpy/estatisticas` |
| 02 · Pandas | 13–18 | `lab/02_pandas.py` | `/produtos` · `/produtos/por-categoria` |
| 03 · Matplotlib / Seaborn | 19–25 | `lab/03_visualizacao.py` | `/produtos/grafico` |
| 04 · APIs (conceitos) | 26–34 | `lab/04_json_xml.py` | `/openapi.json` · `/docs` |
| 05 · requests | 35–42 | `lab/05_requests.py` | *(consome tudo acima)* |
| **06 · FastAPI** | **43–54** | **`main.py`** | **a aula inteira** |
| — · fechamento | 55–56 | — | |
| 07 · Exercício integrado | 57–60 | `lab/07_exercicio.py` · `lab/07_solucao.py` | `/produtos/media` |
| 08 · Quiz | 61–65 | `lab/08_quiz.py` | |

**O slide 6 é o mapa disso** ("Toda essa pilha vira endpoint") e o **slide 53**
é o fecho ("A stack inteira, virada endpoint"). Volte ao slide 6 ao fim de
cada módulo: é o gesto que transforma seis assuntos soltos em uma aula só.

**O fio condutor é um só:** o catálogo de `lab/dados/produtos.csv`
(Notebook R$ 4.500 · Mouse R$ 150 · Monitor R$ 1.200) entra no Pandas no
módulo 02, é calculado no NumPy, vira gráfico no 03, é consumido pelo
`requests` no 05 e é **publicado pela nossa própria API** no 06. O preço
médio de **R$ 1.950,00** e o **Notebook** como produto mais caro aparecem
nos slides e saem iguais na tela — é o mesmo dado.

---

## Preparação (fazer ANTES da aula)

```bash
cd codes/internal/presentation_fast_api
uv sync                                 # instala tudo do pyproject.toml
uv run uvicorn main:app --reload        # deixe rodando num terminal
```

Checklist de guerra:

- [ ] `curl localhost:8000/produtos` responde
- [ ] `localhost:8000/docs` abre no navegador (tela cheia, fonte grande)
- [ ] `localhost:8000/produtos/grafico` mostra o PNG
- [ ] `uv run lab/01_numpy.py` roda até o fim (a medição do final é da SUA máquina)
- [ ] `uv run lab/03_visualizacao.py` abre as janelas de gráfico
- [ ] Terminal com fonte grande (Ctrl+Shift+`+`)
- [ ] `slides/index.html` aberto no navegador (F11 = tela cheia)
- [ ] **Plano B offline:** o único recurso de rede é o CDN do Mermaid (diagramas
      dos slides) e a fonte do Google. Tudo o mais — API, lab, gráficos — roda
      100% local. Se a rede cair, os slides continuam legíveis sem os diagramas.

**Estratégia geral:** navegador com os slides numa metade da tela e o
terminal/editor na outra. Todo slide de código tem o arquivo correspondente
em `lab/` — abra e rode em vez de só mostrar.

---

## Minuto a minuto

Os tempos abaixo somam **≈ 2 h 40 min + intervalo**. Se a aula for mais
curta, os cortes seguros estão marcados com ✂️.

### 0–12 · Abertura (slides 1–6)

Quem sou, o que vamos construir. O **roteiro** (slide 2) e os **objetivos**
(slide 3) — leia rápido, eles servem de mapa para o aluno voltar depois.

O slide 4 (a pilha em camadas) e o 5 (o fluxo) são a espinha dorsal:
**"cada camada resolve um problema e apoia a seguinte"**.

**O slide 6 é o contrato da aula.** Ele mostra que cada camada de hoje já tem
um endereço na nossa API — `/numpy/…`, `/produtos`, `/produtos/grafico`,
`/openapi.json`. Diga com todas as letras:

> *"A nossa parte nesta aula é o FastAPI. Mas FastAPI não é um assunto que
> vem depois dos outros — é onde os outros chegam ao mundo. Tudo o que a
> gente rodar no terminal hoje vai terminar com um endereço."*

Prometa o fecho: *"no fim da aula, o resultado desta análise vai estar
publicado numa API que vocês mesmos escreveram."* Cumpra no slide 53.

### 12–37 · 01 · NumPy (slides 7–12)

Abra `lab/01_numpy.py` e rode. Percorra as seções na ordem.

- **1.1** — o mesmo trabalho, com laço e sem laço. Pergunta à sala:
  *"qual dos dois vocês preferem ler daqui a seis meses?"*
- **1.2** — `shape`, `dtype`, `ndim`. Homogêneo e de tamanho fixo — é daí que
  vem a velocidade.
- **1.3** — vetorização. **Pare na máscara booleana** (`valores > 15`).
  Diga: *"guardem isso, volta no Pandas em vinte minutos"* — e volte mesmo.
- **1.4** — estatística em uma linha. ✂️ dá para acelerar.
- **1.5** — **o momento alto do módulo.** A medição roda ao vivo, na máquina
  do professor. O número (~100x aqui) é real e muda em cada máquina.
  *"O laço do Python paga um custo por elemento. O NumPy paga uma vez."*
- **1.6 — o gancho para a nossa parte.** O script termina chamando
  `GET /numpy/estatisticas` e imprimindo **os mesmos números** do bloco 1.4.
  Volte ao **slide 6** e aponte a linha do NumPy: *"o cálculo é idêntico. O
  que mudou é que agora ele tem um endereço, e qualquer sistema do mundo
  consegue pedir."* Se a API não estiver no ar, o script avisa e segue.

### 37–72 · 02 · Pandas (slides 13–18)

`lab/02_pandas.py`.

- **2.1–2.2** — Series e DataFrame; selecionar e filtrar.
  **Cobre a promessa do módulo 01:** mostre `df["vendas"] > 100` imprimindo
  `[False, True, False]`. *"O filtro do Pandas É a máscara do NumPy."*
- **2.3** — `pd.read_csv()` traz o catálogo de produtos. **A partir daqui é
  sempre este dado.**
- **2.4** — `describe()` e `groupby`. Ao acrescentar o **Teclado**, o
  agrupamento dá exatamente **Acessórios 240 / Informática 5700** — os números
  do slide. Aproveite: acrescentar uma linha é uma aula de Pandas por si só.
- **2.5** — `to_numpy()`, coluna calculada de forma vetorizada.
  **Boa pergunta para a sala:** o produto mais caro é o **Notebook**, mas quem
  mais fatura é o **Mouse**. *"Qual dos dois vocês colocariam na vitrine?"*
- **2.6 — o gancho.** O script consulta `GET /produtos` e
  `GET /produtos/por-categoria`. **Repare no detalhe de ouro:** o servidor
  ainda não tem o Teclado, então o `groupby` da API **não bate** com o do
  terminal. Não conserte — use: *"a tabela do servidor é outra. Daqui a pouco
  a gente cadastra o Teclado por HTTP e esses números se encontram."*
  (E se encontram mesmo, no módulo 06.) Volte ao **slide 6**.

### 72–102 · 03 · Visualização (slides 19–25)

`lab/03_visualizacao.py` — os gráficos abrem em janelas, uma por vez.

- **3.1** — Matplotlib camada a camada.
- **3.2** — os quatro gráficos. Insista: **a escolha vem da pergunta**, não do gosto.
- **3.3–3.4** — Seaborn com `data=df`. O contraste é o ponto: o Matplotlib
  recebe listas soltas; o Seaborn recebe a tabela e os nomes das colunas.
- **3.5** — Seaborn desenha, Matplotlib ajusta. É o padrão real de trabalho.
- **3.6 — o gancho.** O script baixa `GET /produtos/grafico` e salva o PNG.
  *"Uma API não devolve só JSON."* Abra o endereço no navegador, ao vivo.
  Boa deixa para o detalhe técnico: **no servidor não existe tela** — por isso
  o `main.py` escolhe o motor `Agg` antes de tudo. Volte ao **slide 6**.

> ☕ **Intervalo (10 min)** — bom lugar: os dados já foram vistos de ponta a
> ponta, e a segunda metade é sobre APIs.

### 102–127 · 04 · APIs, os conceitos (slides 26–34)

Módulo mais expositivo. `lab/04_json_xml.py` roda a parte concreta.

- **Slide 27** — a virada: *"e de onde os sistemas reais tiram os dados?"*
- **Slide 28** — a analogia do restaurante. **Cliente, garçom, cozinha, cardápio.**
  Insista no cardápio = contrato; ele volta no `/docs` do módulo 06.
- **Slides 30–31** — REST × SOAP, JSON × XML. Rode o `04` e mostre o trabalho
  a mais que o XML dá em Python (procurar cada nó, converter na mão).
- **Slide 32** — métodos. *"O caminho diz o quê; o método diz o que fazer com ele."*
- **Slide 33** — anatomia da requisição/resposta. ✂️ pode ser rápido.
- **Slide 34** — autenticação. Plante a regra: **segredo não vai para o código.**
- **4.5 — o gancho, e talvez o melhor momento da aula.** O script busca
  `GET /openapi.json` da nossa própria API e imprime o contrato: título,
  versão e a lista de caminhos. *"Lembram do cardápio do garçom? É este
  arquivo. E ninguém o escreveu — ele nasceu dos type hints, das classes
  Pydantic e das docstrings."* A analogia do slide 28 deixa de ser metáfora
  na frente da sala. Volte ao **slide 6**.

### 127–157 · 05 · requests (slides 35–42)

**Suba a API antes** (`uv run uvicorn main:app --reload`) e rode
`uv run lab/05_requests.py`.

Diga o que está acontecendo: *"hoje nós somos os dois lados do balcão. Esta
API que estamos consumindo é a que vamos escrever no próximo módulo."*

- **5.1–5.2** — `status_code`, `.json()`, `.text` e a ponte
  `pd.DataFrame(response.json())`. **É o trecho mais repetido da profissão.**
- **5.3** — `params` como dicionário; mostre a URL montada com o acento
  codificado (`Inform%C3%A1tica`).
- **5.4** — `os.getenv`. Repita a regra do slide 34.
- **5.5** — **status ao vivo**: 200, 404, 422, 404-de-rota, um embaixo do outro.
- **5.6** — os três níveis de tratamento de erro. O nível 3 é o de produção.

### 157–197 · 06 · FastAPI (slides 43–54)

**O coração da aula.** Editor com `main.py` de um lado, navegador do outro.

- **Slide 44** — a inversão: `requests` consome, FastAPI cria. *"Uma análise
  que vive só no notebook não é usada por ninguém."*
- **Slides 46–47** — **escreva o hello world do zero**, num arquivo em branco,
  devagar. Decore o comando: `main` = arquivo, `app` = objeto, `--reload` =
  recarrega ao salvar. Depois abra `main.py`, que já está pronto.
- **Slide 48 + seção 4.5 do código** — o type hint validando: `/produtos/1`
  funciona, `/produtos/abc` responde **422**.
- **Slide 49 + seção 2** — Pydantic. Mostre `Field(gt=0)` no preço.

- **Slide 50 — O MOMENTO UAU.** Abra `localhost:8000/docs`:
  - *"Eu não escrevi nenhuma documentação. Nenhuma."*
  - a docstring do endpoint aparecendo como descrição;
  - **Try it out** → executar **dentro da documentação**;
  - `/redoc` e `/openapi.json` de relance — o contrato é um padrão (OpenAPI),
    as duas telas são só visualizações dele.

  **Os erros programados** (o ponto alto, mesmo parecendo o contrário):
  1. `POST /produtos` com `preco: -5` → **422**. *"Não escrevi UM `if`. Foi o `gt=0`."*
  2. Nome com 1 caractere → 422 de novo (`min_length=2`).
  3. `GET /produtos/abc` → 422 ("não é int").
  4. `GET /produtos/999` → **404** — *"esse EU escrevi"* (`HTTPException`).
     Diferença sutil e importante: **422 = pedido malformado** (automático),
     **404 = regra de negócio** (manual).

  **Cadastre o Teclado pelo `/docs`** e volte em `GET /produtos/por-categoria`:
  passa a mostrar **Acessórios 240 / Informática 5700** — exatamente os
  números que o `lab/02_pandas.py` imprimiu no terminal e que a API se
  recusava a dar meia hora atrás. É o encontro que você prometeu no módulo
  02, acontecendo ao vivo, por HTTP. **Este é o momento em que a aula vira
  uma coisa só.**

- **Slide 51 — a pegadinha.** A ordem das rotas. Esta armadilha pegou quem
  escreveu a aula: `/produtos/grafico` respondia **422** porque
  `/produtos/{produto_id}` vinha antes e tentava converter `"grafico"` em int.
  Vale contar que aconteceu de verdade — erro de quem escreveu a aula é o que
  o aluno lembra.
- **Slide 52 + `/estatisticas` e `/produtos/grafico`** — Pandas, NumPy e
  Matplotlib **dentro** do endpoint. *"É assim que modelos de ML chegam à
  produção."* Abra `/produtos/grafico` no navegador: uma API não devolve só JSON.
- **Slide 53 — o fecho da promessa.** Depois de percorrer o `main.py`, abra
  o slide 53 e mostre o desenho: as quatro seções da nossa API são as quatro
  camadas da aula. Feche com a frase que o slide traz:
  **"o FastAPI não substitui a sua análise — ele a entrega."**
  Nenhuma conta foi reescrita: o `mean()` é o do módulo 01, o `groupby` é o
  do 02. Se sobrar tempo, mostre as seções 4.2 e 4.3 do `main.py` lado a lado
  com `lab/01_numpy.py` e `lab/02_pandas.py`.
- **Slide 54** — boas práticas. ✂️ leitura rápida, é material de consulta.

### 197–202 · Fechamento da stack (slides 55–56)

O diagrama da pilha completa e a tese: **Ciência de Dados não termina no
DataFrame.** Deixe o slide 56 no ar enquanto respira.

### 202–227 · 07 · Exercício integrado (slides 57–60)

Slide 58 = enunciado. Mande abrir `lab/07_exercicio.py`, que tem os seis
passos como TODO e **funciona mesmo sem a API no ar** (cai para a lista em
Python, como a dica do enunciado manda).

Circule pela sala. Depois abra `lab/07_solucao.py` e rode: sai
**R$ 1.950,00** e **Notebook** — os números do slide, ao vivo.

⚠️ Se você cadastrou o Teclado na demo do módulo 06, **reinicie o servidor**
antes: o "banco" é um DataFrame em memória. Isso é uma boa deixa —
*"repararam que os dados sumiram? É por isso que existe banco de dados."*

### 227–242 · 08 · Quiz e encerramento (slides 61–65)

`uv run lab/08_quiz.py` roda o quiz no terminal, com correção; ou use os
slides 60–62. As quatro perguntas abertas valem mais discutidas do que
respondidas.

Feche no slide 65 e no dever de casa: **escolha uma API pública, traga os
dados para um DataFrame e publique um resultado seu.**

---

## Perguntas prováveis (respostas prontas)

- **"Isso escala? O banco é um DataFrame em memória!"** — "Não escala mesmo, é
  didático. Ele é um 'repositório': amanhã vira SQLite/Postgres mudando poucas
  linhas — e **nenhuma** das rotas."
- **"Por que `def` e não `async def`?"** — "O FastAPI aceita os dois; `async` é
  para quando você espera I/O concorrente. Fica de dever de casa."
- **"Por que `float()` no retorno?"** — "O Pandas devolve `np.float64` e o JSON
  quer número do Python. É o tipo de detalhe que só aparece quando se publica."
- **"Dá para devolver o gráfico em vez do número?"** — "Dá, e já está feito:
  `/produtos/grafico`. Uma API não devolve só JSON."
- **"Serve para produção?"** — "Serve. Falta persistência, autenticação, testes
  e CI — exatamente a disciplina de MLOps."

## Se algo quebrar ao vivo

- **Porta ocupada** (`address already in use`) → `uv run uvicorn main:app --reload --port 8001`
  (e ajuste: `URL_BASE=http://127.0.0.1:8001 uv run lab/05_requests.py`).
- **`--reload` não recarrega** → salvou o arquivo certo? Reinicie o uvicorn.
- **422 inesperado** → leia a resposta: o FastAPI diz EXATAMENTE o campo e o
  motivo. Transforme a leitura do 422 em demonstração, não em erro.
- **Rota nova responde 422 sem motivo** → é a pegadinha do slide 51: alguma
  rota com `{parâmetro}` está declarada antes dela.
- **Gráfico não abre** (máquina sem tela) → os scripts detectam e salvam em
  `lab/saida/*.png`. Abra os PNGs.
- **Nada funciona** → abra os arquivos no editor e continue por eles; os
  conceitos não dependem do servidor no ar.
