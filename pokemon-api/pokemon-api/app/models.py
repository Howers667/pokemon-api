from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Tabela de associação: um pokémon tem 1..N tipos, um tipo pertence a N pokémons.
pokemon_types = Table(
    "pokemon_types",
    Base.metadata,
    Column("pokemon_id", ForeignKey("pokemons.id", ondelete="CASCADE"), primary_key=True),
    Column("type_id", ForeignKey("types.id", ondelete="CASCADE"), primary_key=True),
)


class Type(Base):
    __tablename__ = "types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)


class Pokemon(Base):
    __tablename__ = "pokemons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hp: Mapped[int] = mapped_column(Integer)
    attack: Mapped[int] = mapped_column(Integer)
    defense: Mapped[int] = mapped_column(Integer)
    speed: Mapped[int] = mapped_column(Integer)
    height: Mapped[float] = mapped_column()  # metros
    weight: Mapped[float] = mapped_column()  # quilos

    types: Mapped[list[Type]] = relationship(secondary=pokemon_types, lazy="selectin")
