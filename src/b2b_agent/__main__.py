import sys

#from .research import pesquisar_empresa
from .agent import pesquisar_empresa_com_agente

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
        resultado = pesquisar_empresa_com_agente(empresa)
        print(resultado.model_dump_json(indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())