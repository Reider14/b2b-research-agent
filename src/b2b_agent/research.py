from .llm import structured_completion
from .schema import Empresa

SYSTEM_PROMPT = (
    "Voce e um analista de pesquisa B2B rigoroso. Responda sempre em portugues. "
    "Nunca invente informacoes: se nao conhecer a empresa ou nao tiver certeza, "
    "defina nivel_confianca como 'baixo' e deixe claro no resumo que nao ha dados suficientes."
)

def pesquisar_empresa(nome_empresa: str) -> Empresa:
    return structured_completion(
        system=SYSTEM_PROMPT,
        user=f'Analise a empresa "{nome_empresa}"',
        schema=Empresa,
    )