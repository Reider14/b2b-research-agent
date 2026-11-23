import json

BASE_CONHECIMENTO = {
    "microsoft": {
        "nome": "Microsoft",
        "setor": "Tecnologia",
        "funcionarios": 228000,
        "descricao": "Software, nuvem (Azure), jogos e dispositivos.",
    },
    "meta": {
        "nome": "Meta Platforms",
        "setor": "Tecnologia",
        "funcionarios": 74000,
        "descricao": "Redes sociais (Facebook, Instagram, WhatsApp) e realidade virtual.",
        "nome_anterior": "Facebook, Inc.",
    },
}

ALIASES = { "facebook": "meta" }

FONTE = "base_local_testes"

def buscar_empresa(nome: str) -> str:
    chave = nome.strip().lower()
    chave = ALIASES.get(chave, chave)
    dados = BASE_CONHECIMENTO.get(chave)
    if dados is None:
        return json.dumps(
            {
                "encontrado": False, 
                "fonte": FONTE,
                "mensagem": f"Nenhum dado sobre '{nome}'."
            }
        )
    return json.dumps(
        {
            "encontrado": True,
            "fonte": FONTE,
            **dados
        }
    )

TOOLS = {
    "type": "function",
    "function": {
        "name": "buscar_empresa",
        "description": (
            "Busca dados de uma empresa na base de conhecimento. "
            "Use sempre antes de responder. Se encontrado for false, "
            "nao ha dados confiaveis sobre a empresa."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "description": "Nome da empresa",
                },
                "required": ["nome"]
            }
        }
    }

}

FUNCOES = {"buscar_empresa": buscar_empresa}

def executar_ferramenta(nome: str, argumentos_json: str) -> str:
    funcao = FUNCOES.get(nome)
    if funcao is None:
        return json.dumps({"erro": f"Ferramenta desconhecida: {nome}"})
    try:
        argumentos = json.loads(argumentos_json)
        return funcao(**argumentos)
    except Exception as e:
        return json.dumps({"erro": f"Falha ao executar {nome}"})