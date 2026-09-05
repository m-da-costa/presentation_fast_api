# SentimentAPI — demo FastAPI para a aula (PUC)

Demo de ~40 min: um "hello world com dados e IA" que um iniciante acompanha.
Uma API de avaliações de filmes com análise de sentimento em português,
escrita em **um único `main.py`** com comentários didáticos.

O objetivo pedagógico é mostrar o superpoder do FastAPI: **type hints,
classes Pydantic e docstrings viram validação e documentação (Swagger)
automáticas**.

## Rodar

```bash
python -m venv .venv && source .venv/bin/activate   # ou: uv venv
pip install -r requirements.txt                      # ou: uv pip install -r requirements.txt
uvicorn main:app --reload
```

| URL | O que é |
|---|---|
| http://127.0.0.1:8000 | a API em si |
| http://127.0.0.1:8000/docs | **Swagger UI** interativa (a estrela da demo) |
| http://127.0.0.1:8000/redoc | ReDoc (documentação alternativa) |
| http://127.0.0.1:8000/openapi.json | o contrato OpenAPI gerado |

## Roteiro da demo (arquivos)

- `main.py` — a aplicação, numerada em seções 1–4 para acompanhar a aula.
- `AULA.md` — roteiro do instrutor com timing, falas e o momento "uau".
- `slides/` — apresentação HTML autocontida.

## Endpoints

| Método | Rota | Ensina o quê |
|---|---|---|
| GET | `/` | hello world; dict → JSON |
| GET | `/ola/{nome}` | parâmetro de rota |
| POST | `/avaliacoes` | corpo JSON + validação Pydantic + `response_model` + status 201 |
| GET | `/avaliacoes` | query strings opcionais + filtro |
| GET | `/avaliacoes/{id}` | conversão automática de tipo + `HTTPException` 404 |
| GET | `/predizer?texto=…` | a "IA" via query string |
| POST | `/predizer` | a "IA" via corpo JSON (contraste: dict cru vs Pydantic) |
| GET | `/estatisticas` | agregação de dados |

## Experimentos que dão certo na demo

1. `GET /ola/PUC` → `{"mensagem": "Olá, PUC! 👋"}`
2. `GET /ola/` → 404 (parâmetro obrigatório)
3. `POST /avaliacoes` com `nota: 42` → **422 automático** (o Field(ge=1, le=5))
4. `POST /avaliacoes` texto *"Filme maravilhoso, adorei demais"* → sentimento positivo
5. `POST /avaliacoes` texto *"Chato, cansativo, perdi tempo"* → negativo
6. `GET /avaliacoes?nota_minima=99` → 422 na query string
7. `GET /avaliacoes/999` → 404 com mensagem amigável
8. `GET /estatisticas` → contagem por sentimento + nota média

A "IA" é um classificador por léxico em Python puro — legível por quem
nunca viu ML. Para a próxima aula, o gancho natural é trocar `classificar()`
por um modelo scikit-learn treinado: a API não muda.
