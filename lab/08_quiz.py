"""
MÓDULO 08 · Quiz de fechamento
==============================

Sete perguntas rápidas para fixar o conteúdo.

Rode assim:

    uv run lab/08_quiz.py              # responder
    uv run lab/08_quiz.py --respostas  # só o gabarito
"""

import sys

FECHADAS = [
    (
        "1. Qual biblioteca é especializada em manipulação de dados tabulares?",
        {"A": "NumPy", "B": "Pandas", "C": "Requests", "D": "FastAPI"},
        "B",
        "NumPy trabalha com arrays; Pandas com tabelas.",
    ),
    (
        "2. Qual método HTTP normalmente é usado para consultar dados?",
        {"A": "POST", "B": "DELETE", "C": "GET", "D": "PUT"},
        "C",
        "GET consulta sem alterar dados no servidor.",
    ),
    (
        "3. Qual biblioteca usamos para consumir uma API?",
        {"A": "requests", "B": "matplotlib", "C": "numpy", "D": "fastapi"},
        "A",
        "requests consome; FastAPI cria.",
    ),
]

ABERTAS = [
    (
        "4. O que significa o código HTTP 404?",
        "Recurso não encontrado — o caminho pedido não existe na API.",
    ),
    (
        "5. Qual é o papel do FastAPI?",
        "Criar APIs: expor dados e resultados como endpoints HTTP.",
    ),
    (
        "6. Qual é a relação entre Pandas e APIs?",
        "A API entrega JSON; o Pandas transforma esse JSON em DataFrame "
        "para análise.",
    ),
    (
        "7. Qual seria o fluxo completo para buscar dados de uma API e "
        "gerar um gráfico?",
        "requests.get → response.json() → pd.DataFrame → análise → "
        "Matplotlib/Seaborn.",
    ),
]


def gabarito() -> None:
    print("\n" + "=" * 66)
    print("GABARITO")
    print("=" * 66)
    for pergunta, alternativas, correta, porque in FECHADAS:
        print(f"\n{pergunta}")
        print(f"  ✅ {correta}) {alternativas[correta]} — {porque}")
    for pergunta, resposta in ABERTAS:
        print(f"\n{pergunta}")
        print(f"  ✅ {resposta}")


def responder() -> None:
    acertos = 0
    print("=" * 66)
    print("08 · QUIZ DE FECHAMENTO")
    print("=" * 66)

    for pergunta, alternativas, correta, porque in FECHADAS:
        print(f"\n{pergunta}")
        for letra, texto in alternativas.items():
            print(f"  {letra}) {texto}")
        escolha = input("  sua resposta: ").strip().upper()[:1]
        if escolha == correta:
            acertos += 1
            print(f"  ✅ isso! {porque}")
        else:
            print(f"  ❌ era {correta}) {alternativas[correta]} — {porque}")

    print(f"\n>>> {acertos}/{len(FECHADAS)} nas fechadas.")
    print("\nAgora as abertas — responda com suas palavras (Enter para ver):")
    for pergunta, resposta in ABERTAS:
        print(f"\n{pergunta}")
        input("  pressione Enter para ver uma resposta possível... ")
        print(f"  💡 {resposta}")

    print("\n" + "=" * 66)
    print("O QUE LEVAR DESTA AULA")
    print("=" * 66)
    for nome, papel in [
        ("NumPy", "cálculo vetorizado — a base numérica"),
        ("Pandas", "a tabela onde a análise acontece"),
        ("Matplotlib / Seaborn", "o gráfico que revela o que o número esconde"),
        ("requests", "a porta de entrada dos dados"),
        ("FastAPI", "a porta de saída do seu trabalho"),
    ]:
        print(f"  {nome:<22} {papel}")
    print(
        "\nPróximo passo: escolha uma API pública, traga os dados para um\n"
        "DataFrame e publique um resultado seu."
    )


if __name__ == "__main__":
    if "--respostas" in sys.argv:
        gabarito()
    else:
        try:
            responder()
        except (EOFError, KeyboardInterrupt):
            print("\n\n(sem terminal interativo — mostrando o gabarito)")
            gabarito()
