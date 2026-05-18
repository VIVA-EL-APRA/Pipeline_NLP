import argparse
import json
import sys

from nlp_pipeline import DEFAULT_TEXT, NLPipeline


def print_section(title):
    lineo = "=" * len(title)
    print(f"\n{lineo}\n{title}\n{lineo}")


def main():
    parser = argparse.ArgumentParser(description="Pipeline NLP clasico con spaCy")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Texto a procesar")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    try:
        pipeline = NLPipeline()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    resultado = pipeline.procesar(args.text)

    if args.json:
        json.dump(resultado, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return

    print_section("Texto bruto")
    print(args.text)

    print_section("1. Segmentacion en frases")
    print(f"Total de frases detectadas: {len(resultado['frases'])}")
    for i, frase in enumerate(resultado["frases"], 1):
        print(f"[{i}] {frase}")

    print_section("2. Tokenizacion")
    print(f"Total de tokens: {len(resultado['tokens'])}")
    for i, token in enumerate(resultado["tokens"], 1):
        print(f"[{i}] {token}")

    print_section("3. Lematizacion")
    for item in resultado["lemas"]:
        print(f"{item['token']:<20} -> {item['lemma']}")

    print_section("4. POS Tagging")
    for item in resultado["pos"]:
        print(f"{item['token']:<20} [{item['eagles']}] {item['explicacion']}")

    print_section("5. Quitar stopwords")
    print(f"Total de tokens sin stopwords: {len(resultado['sin_stopwords'])}")
    for i, item in enumerate(resultado["sin_stopwords"], 1):
        print(f"[{i}] token={item['token']} | lemma={item['lemma']} | pos={item['eagles']}")


if __name__ == "__main__":
    main()
