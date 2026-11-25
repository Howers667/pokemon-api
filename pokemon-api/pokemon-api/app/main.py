from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registra os modelos no metadata)
from app.database import Base, engine
from app.routers import pokemons


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Pokémon API",
    description="API REST para gerenciar pokémons, inspirada na PokéAPI.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(pokemons.router)


@app.get("/", tags=["Health"], summary="Health check")
def health():
    return {"status": "ok"}
