import sys

from .research import pesquisar_empresa

EMPRESAS = [
    "Microsoft",
    "Kestrel Quantun Logistics",
    "Meta",
    "Amazon",
    "Facebook",
]

def main() -> int:
    for empresa in sys.argv[1:] or EMPRESAS:
        print(f"\nA pesquisar empresa: {empresa} ...")
        resultado = pesquisar_empresa(empresa)
        print(resultado.model_dump_json(indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())