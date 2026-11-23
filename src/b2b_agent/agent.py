import json
from openai import OpenAI
from .llm import MODEL, get_client
from .schema import Empresa
from .tools import TOOLS, executar_ferramenta

MAX_STEP = 5

SYSTEM_PROMPT = (
    "Voce e um analista de pesquisa B2B rigoroso. Responda sempre em portugues. "
    "Use SEMPRE a ferramenta buscar_empresa antes de responder. "
    "Use apenas dados retornados pelas ferramentas. Se a ferramenta nao encontrar "
    "a empresa, defina nivel_confianca como 'baixo', estimativa_funcionarios como null "
    "e diga no resumo que nao ha dados suficientes. Nunca invente informacoes."
)


def pesquisar_empresa_com_agente(nome_empresa: str) -> Empresa:
    client = get_client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f'Analise a empresa "{nome_empresa}"'},
    ]

    for passo in range(1, MAX_STEP + 1):
        completion = client.chat.completions.parse(
            model=MODEL,
            temperature=0,
            messages=messages,
            tools=TOOLS,
            response_format=Empresa 
        )
        message = completion.choices[0].message

        if not message.tool_calls:
            if message.refusal:
                raise RuntimeError(f"O modelo recusou a requisicao: {message.refusal}")
            if message.parsed is None:
                raise RuntimeError("Resposta final vazia ou fora do contrato.")
            return message.parsed

        messages.append(message)
        for chamada in message.tool_calls:
            print(f"[passp {passo}] ferramenta: {chamada.function.name}({chamada.function.arguments})")
            resultado = executar_ferramenta(chamada.function.name, chamada.function.arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": chamada.id,
                    "content": resultado
                }
            )

    raise RuntimeError(f"O agente nao termminou em {MAX_STEP} passos.")