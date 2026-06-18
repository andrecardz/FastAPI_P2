from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProdutoCreate(BaseModel):
    nome: str = Field(min_length=1)
    preco: float = Field(gt=0)
    estoque: int = Field(default=0, ge=0)
    ativo: bool = True

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value):
        if not value.strip():
            raise ValueError("Nome não pode ser vazio")
        return value.strip()


class ProdutoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    preco: float
    estoque: int
    ativo: bool
