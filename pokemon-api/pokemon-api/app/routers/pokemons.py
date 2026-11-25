from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/pokemons", tags=["Pokémons"])

NOT_FOUND = {404: {"description": "Pokémon não encontrado"}}
CONFLICT = {409: {"description": "Já existe um pokémon com esse nome"}}


@router.post(
    "",
    response_model=schemas.PokemonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar pokémon",
    description="Cadastra um novo pokémon. Os tipos são criados automaticamente se ainda não existirem.",
    responses=CONFLICT,
)
def create_pokemon(data: schemas.PokemonCreate, db: Session = Depends(get_db)):
    if crud.get_pokemon_by_name(db, data.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um pokémon com esse nome")
    return crud.create_pokemon(db, data)


@router.get(
    "",
    response_model=list[schemas.PokemonResponse],
    summary="Listar pokémons",
    description="Lista pokémons com paginação (`skip`/`limit`) e filtro opcional por tipo.",
)
def list_pokemons(
    skip: int = Query(0, ge=0, description="Quantos registros pular"),
    limit: int = Query(20, ge=1, le=100, description="Máximo de registros retornados"),
    type: str | None = Query(None, description="Filtra por tipo, ex.: fire"),
    db: Session = Depends(get_db),
):
    return crud.list_pokemons(db, skip=skip, limit=limit, type_name=type)


@router.get(
    "/{pokemon_id}",
    response_model=schemas.PokemonResponse,
    summary="Buscar pokémon por ID",
    responses=NOT_FOUND,
)
def get_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    pokemon = crud.get_pokemon(db, pokemon_id)
    if pokemon is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pokémon não encontrado")
    return pokemon


@router.patch(
    "/{pokemon_id}",
    response_model=schemas.PokemonResponse,
    summary="Atualizar pokémon",
    description="Atualização parcial: envie somente os campos que deseja alterar.",
    responses={**NOT_FOUND, **CONFLICT},
)
def update_pokemon(
    pokemon_id: int, data: schemas.PokemonUpdate, db: Session = Depends(get_db)
):
    pokemon = crud.get_pokemon(db, pokemon_id)
    if pokemon is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pokémon não encontrado")
    if data.name and data.name != pokemon.name and crud.get_pokemon_by_name(db, data.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Já existe um pokémon com esse nome")
    return crud.update_pokemon(db, pokemon, data)


@router.delete(
    "/{pokemon_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir pokémon",
    responses=NOT_FOUND,
)
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    pokemon = crud.get_pokemon(db, pokemon_id)
    if pokemon is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pokémon não encontrado")
    crud.delete_pokemon(db, pokemon)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
