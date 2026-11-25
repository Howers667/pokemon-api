from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def _get_or_create_types(db: Session, names: list[str]) -> list[models.Type]:
    result = []
    for name in names:
        t = db.scalar(select(models.Type).where(models.Type.name == name))
        if t is None:
            t = models.Type(name=name)
            db.add(t)
        result.append(t)
    return result


def get_pokemon(db: Session, pokemon_id: int) -> models.Pokemon | None:
    return db.get(models.Pokemon, pokemon_id)


def get_pokemon_by_name(db: Session, name: str) -> models.Pokemon | None:
    return db.scalar(select(models.Pokemon).where(models.Pokemon.name == name))


def list_pokemons(
    db: Session, skip: int = 0, limit: int = 20, type_name: str | None = None
) -> list[models.Pokemon]:
    stmt = select(models.Pokemon).order_by(models.Pokemon.id).offset(skip).limit(limit)
    if type_name:
        stmt = stmt.where(
            models.Pokemon.types.any(models.Type.name == type_name.strip().lower())
        )
    return list(db.scalars(stmt))


def create_pokemon(db: Session, data: schemas.PokemonCreate) -> models.Pokemon:
    payload = data.model_dump(exclude={"types"})
    pokemon = models.Pokemon(**payload, types=_get_or_create_types(db, data.types))
    db.add(pokemon)
    db.commit()
    db.refresh(pokemon)
    return pokemon


def update_pokemon(
    db: Session, pokemon: models.Pokemon, data: schemas.PokemonUpdate
) -> models.Pokemon:
    changes = data.model_dump(exclude_unset=True)
    type_names = changes.pop("types", None)
    for field, value in changes.items():
        setattr(pokemon, field, value)
    if type_names is not None:
        pokemon.types = _get_or_create_types(db, type_names)
    db.commit()
    db.refresh(pokemon)
    return pokemon


def delete_pokemon(db: Session, pokemon: models.Pokemon) -> None:
    db.delete(pokemon)
    db.commit()
