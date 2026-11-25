from pydantic import BaseModel, ConfigDict, Field, field_validator


class PokemonBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, examples=["pikachu"])
    hp: int = Field(..., ge=1, le=255, examples=[35])
    attack: int = Field(..., ge=1, le=255, examples=[55])
    defense: int = Field(..., ge=1, le=255, examples=[40])
    speed: int = Field(..., ge=1, le=255, examples=[90])
    height: float = Field(..., gt=0, description="Altura em metros", examples=[0.4])
    weight: float = Field(..., gt=0, description="Peso em quilos", examples=[6.0])
    types: list[str] = Field(..., min_length=1, max_length=2, examples=[["electric"]])

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("types")
    @classmethod
    def normalize_types(cls, v: list[str]) -> list[str]:
        return list(dict.fromkeys(t.strip().lower() for t in v if t.strip()))


class PokemonCreate(PokemonBase):
    pass


class PokemonUpdate(BaseModel):
    """Atualização parcial: envie apenas os campos que deseja alterar."""

    name: str | None = Field(None, min_length=1, max_length=50)
    hp: int | None = Field(None, ge=1, le=255)
    attack: int | None = Field(None, ge=1, le=255)
    defense: int | None = Field(None, ge=1, le=255)
    speed: int | None = Field(None, ge=1, le=255)
    height: float | None = Field(None, gt=0)
    weight: float | None = Field(None, gt=0)
    types: list[str] | None = Field(None, min_length=1, max_length=2)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v):
        return v.strip().lower() if v else v

    @field_validator("types")
    @classmethod
    def normalize_types(cls, v):
        return list(dict.fromkeys(t.strip().lower() for t in v if t.strip())) if v else v


class PokemonResponse(PokemonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., examples=[25])

    @field_validator("types", mode="before")
    @classmethod
    def types_to_names(cls, v):
        # Converte objetos Type do SQLAlchemy em lista de nomes
        return [t.name if hasattr(t, "name") else t for t in v]
