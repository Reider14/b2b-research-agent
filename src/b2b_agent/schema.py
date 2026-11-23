from pydantic import BaseModel, Field
from typing import Literal

class Empresa(BaseModel): 
    nome: str
    setor: str
    tecnologias: list[str]
    resumo_modelo_negocio: str = Field(
        description="Resuma o modelo de negocio em no maximo 2 frases"
    )
    estimativa_funcionarios: int | None = Field(
        description="Estimativa aproximada. Use null se nao souber."
    )
    nivel_confianca: Literal["alto", "medio", "baixo"] = Field(
        description="Nivel de certeza sobre os dados informados."
    )


