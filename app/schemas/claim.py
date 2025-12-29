from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ClaimType(str, Enum):
    AUTO = "automovel"
    RESIDENCIAL = "residencial"
    VIDA = "vida"
    OUTROS = "outros"

class EmailProcessRequest(BaseModel):
    subject: str = Field(description="Assunto do e-mail")
    body: str = Field(description="Corpo do e-mail")

class ClaimExtraction(BaseModel):
    tipo_sinistro: ClaimType = Field(description="O ramo do seguro que o sinistro pertence")
    resumo: str = Field(description="Um resumo de uma frase sobre o que aconteceu")
    data_ocorrido: Optional[str] = Field(None, description="A data da ocorrência do sinistro, pode vir no formato de texto por exemplo (hoje, ontem, etc) retorne em formato de data")
    placa_veiculo: Optional[str] = Field(None, description="Placa do carro, se for sinistro de Auto")
    local_evento: Optional[str] = Field(None, description="Endereço ou local do ocorrido")
    nivel_urgencia: str = Field(description="Avaliação de urgência: Baixa, Média ou Alta")
    