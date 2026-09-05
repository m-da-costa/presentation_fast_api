# AULA.md — Roteiro do instrutor (demo FastAPI, PUC)

**Duração:** 40 min · **Formato:** demo ao vivo (o professor programa, os alunos acompanham) · **Público:** iniciantes absolutos · **Idioma:** PT-BR

**Objetivo de aprendizagem:** ao final, o aluno entende que no FastAPI
**type hints, classes Pydantic e docstrings não são decoração — são o
contrato e a documentação da API**, e consegue rodar e estender o hello world.

---

## Preparação (fazer ANTES da aula, no hotel de casa)

```bash
cd codes/internal/presentation_fast_api
uv venv && source .venv/bin/activate     # ou python -m venv .venv
uv pip install -r requirements.txt       # ou pip install -r requirements.txt
uvicorn main:app --reload                # deixe rodando num terminal
```

Checklist de guerra:

- [ ] `curl localhost:8000/ola/PUC` responde
- [ ] `localhost:8000/docs` abre no navegador (tela cheia, fonte grande)
- [ ] Os 2 primeiros POSTs de teste já foram feitos (para /estatisticas não vir vazio)
- [ ] Terminal com fonte grande (Ctrl+Shift+ `+`), tema claro para contraste no projetor
- [ ] Plano B offline: a API roda 100% local, sem internet. Só o CDN dos slides usa rede —
      se cair, ensine pelo `main.py` aberto no editor.
- [ ] `main.py` aberto no editor ao lado do navegador (metade e metade na tela)

**Estratégia geral:** navegador com `/docs` na metade da tela, editor com `main.py`
na outra. Toda seção do código tem número (1–4) — navegue pelo número.

---

## Minuto a minuto

### 0–5 · Abertura (slides 1–4)

Quem sou, o que vamos construir: **uma API que lê avaliações de filmes e diz se
o sentimento é positivo ou negativo — com "IA" e tudo — em 40 minutos.**

Analogia do garçom (slide 3): cliente pede, cozinha prepara, **cardápio é o
contrato**. API = garçom; FastAPI = o garçom que ainda por cima escreve o
cardápio sozinho e confere os pedidos.

Por que FastAPI e não Flask/Django (slide 4): type hints, validação e
documentação automáticas, async, performance. Não denegrir os outros —
"é o queridinho de quem faz IA hoje porque conversa com Python moderno".

### 5–12 · Hello world ao vivo (slides 5–6, código seção 4.1)

Não copie ainda — **escreva do zero** num arquivo em branco, devagar:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def raiz():
    return {"mensagem": "Olá, PUC!"}
```

Rode: `uvicorn main:app --reload`. Decore o comando:
`main` = arquivo, `app` = objeto lá dentro, `--reload` = recarrega ao salvar.

Abra `localhost:8000` → o JSON. **Pergunta à sala:** "quantas linhas pra servir
isso na web aí no seu framework favorito?"

Depois adicione `/ola/{nome}` mostrando o parâmetro de rota. Teste `/ola/PUC`.

### 12–22 · O MOMENTO UAU: /docs (slide 7)

**Aqui está a aula inteira.** Abra `localhost:8000/docs`.

- "Eu não escrevi nenhuma documentação. Nenhuma."
- Mostre a docstring do endpoint aparecendo como descrição.
- Clique num endpoint, "Try it out", execute — **dentro da documentação**.
- Mostre `/redoc` e `/openapi.json` rapidinho — o contrato é um padrão
  (OpenAPI), as duas telas são só visualizações dele.

Gancho: "como ele sabe o que cada endpoint recebe e devolve? Adivinhem:
estava no código o tempo todo."

### 22–30 · Type hints e Pydantic: o contrato (slides 8–9, código seções 2 e 4.2)

Volte ao `main.py` (que já está pronto — economize tempo). Seção 2:
a classe `AvaliacaoEntrada`. Mostre `Field(ge=1, le=5)` na nota.

**Os erros programados (o contrário do que parece, são o ponto alto):**

1. `POST /avaliacoes` pelo Swagger com `nota: 42` → **422**. "Eu não escrevi
   UM IF de validação. Foi o `le=5`."
2. Texto de 2 caracteres → 422 de novo (`min_length=3`).
3. `GET /avaliacoes/abc` → 422 ("não é int").
4. `GET /avaliacoes/999` → 404 — "esse EU escrevi" (`HTTPException`).
   Diferença sutil e importante: 422 = pedido malformado (automático),
   404 = regra de negócio (manual).

Cadastre as duas avaliações (pelo /docs, Try it out):

```json
{"texto": "Filme maravilhoso, adorei demais! Recomendo.", "nota": 5, "autor": "Maria"}
{"texto": "Chato, cansativo, perdi tempo. Péssimo.", "nota": 1, "autor": "João"}
```

Mostre a resposta com `sentimento` e `confianca` preenchidos.

### 30–37 · A mini-IA + dados (slides 10–11, seções 1 e 4.3–4.4)

Volte ao topo do `main.py`: o léxico e `classificar()`. Percorra linha a
linha — tokeniza, soma pesos, decide. "É IA de brinquedo, e é o ponto:
vocês entenderam TODAS as linhas. Na próxima aula troco isso por
scikit-learn e **a API nem percebe** — o modelo é detalhe de implementação."

Feche com dados:

- `GET /avaliacoes?sentimento=positivo` (query string)
- `GET /predizer?texto=Amei, excelente!` (a IA direto na URL, sem POST)
- `GET /estatisticas` — contagem por sentimento + nota média

### 37–40 · Fechamento (slide 12)

Recapitule a tese: **o código é a documentação**. Dever de casa:
trocar o léxico por um modelo, persistir em banco, subir com Docker.
Cada um puxa no GitHub. Agradeça.

---

## Perguntas prováveis (respostas prontas)

- **"Isso escala? O banco é um dict!"** — "Não escala mesmo, é didático.
  O dict é um 'repositório' — amanhã vira SQLite/Postgres mudando umas 3 linhas."
- **"Por que `def` e não `async def`?** — "FastAPI aceita os dois; `async`
  é para quando você espera I/O concorrente. Dever de casa."
- **"Isso é IA de verdade?"** — "É baseline de NLP — léxico foi estado da
  arte por décadas. O gancho é: o modelo é plugável."
- **"Serve para produção?"** — "Serve. Falta persistência, auth, testes,
  CI — exatamente a disciplina de MLOps do professor Leonardo."

## Se algo quebrar ao vivo

- **Erro de porta** (`address already in use`) → `uvicorn main:app --reload --port 8001`.
- **--reload não recarrega** → salvou o arquivo certo? Reinicie o uvicorn.
- **422 inesperado** → leia a resposta: o FastAPI diz EXATAMENTE o campo e o motivo. Vire a leitura do 422 em demonstração, não em erro.
- **Nada funciona** → abra o `main.py` e continue a aula por ele; os conceitos não dependem do servidor no ar.
