from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent

TESTES = [

    (
        "Template Validator",
        "tools/validate_templates.py",
    ),

    (
        "Content Check",
        "tools/content_check.py",
    ),

    (
        "Stress Test",
        "tools/stress_test.py",
    ),

    (
        "Distribution Analyzer",
        "tools/analyze_distribution.py",
    ),

]


def banner():

    print()
    print("=" * 70)
    print("BOT ANELAS - PRE RELEASE CHECK")
    print("=" * 70)
    print()


def executar(nome, script):

    print(f"▶ {nome}")

    inicio = time.perf_counter()

    resultado = subprocess.run(
        [
            sys.executable,
            str(ROOT / script),
        ]
    )

    tempo = time.perf_counter() - inicio

    ok = resultado.returncode == 0

    status = "✅ PASSOU" if ok else "❌ FALHOU"

    print(f"{status} ({tempo:.2f}s)")
    print()

    return ok, tempo


def main():

    banner()

    aprovados = 0

    tempos = []

    for nome, script in TESTES:

        ok, tempo = executar(
            nome,
            script,
        )

        tempos.append(tempo)

        if ok:
            aprovados += 1

    print("=" * 70)

    print("RESUMO")

    print("=" * 70)

    print()

    print(f"Testes: {aprovados}/{len(TESTES)}")

    print(f"Tempo total: {sum(tempos):.2f}s")

    print()

    if aprovados == len(TESTES):

        print("🎉 BOT APROVADO PARA RELEASE")

    else:

        print("⚠ Existem testes falhando.")

        sys.exit(1)


if __name__ == "__main__":
    main()