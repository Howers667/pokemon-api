# Pokémon API

API REST para gerenciar pokémons (inspirada na PokéAPI), construída com **FastAPI**, **SQLAlchemy 2.0** e **PostgreSQL**, containerizada com **Docker**.

## Tecnologias

- Python 3.12 · FastAPI · Pydantic v2
- SQLAlchemy 2.0 (ORM) · PostgreSQL 16
- Docker e docker-compose
- Pytest + TestClient (banco SQLite em memória nos testes)

## Como rodar (Docker)

```bash
cp .env.example .env      # ajuste usuário/senha se quiser
docker compose up --build
```

- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Para parar: `docker compose down` (use `-v` para apagar também o volume do banco).

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `POSTGRES_USER` | Usuário do PostgreSQL |
| `POSTGRES_PASSWORD` | Senha do PostgreSQL |
| `POSTGRES_DB` | Nome do banco |
| `DATABASE_URL` | Montada automaticamente pelo `docker-compose.yml`. Sem ela, a API usa SQLite local |

O arquivo `.env` **não** é versionado; use o `.env.example` como referência.

## Testes

Com Docker (API já em pé):
```bash
docker compose exec api pytest -v
```

Localmente:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## Endpoints

| Método | Rota | Descrição | Respostas |
|---|---|---|---|
| POST | `/pokemons` | Cria pokémon | 201, 409, 422 |
| GET | `/pokemons` | Lista (params: `skip`, `limit`, `type`) | 200 |
| GET | `/pokemons/{id}` | Busca por ID | 200, 404 |
| PATCH | `/pokemons/{id}` | Atualização parcial | 200, 404, 409, 422 |
| DELETE | `/pokemons/{id}` | Exclui | 204, 404 |
| GET | `/` | Health check | 200 |

### Exemplo

```bash
curl -X POST http://localhost:8000/pokemons \
  -H "Content-Type: application/json" \
  -d '{"name":"pikachu","hp":35,"attack":55,"defense":40,"speed":90,"height":0.4,"weight":6.0,"types":["electric"]}'
```

## Modelo de dados

- `pokemons` (id, name único, hp, attack, defense, speed, height, weight)
- `types` (id, name único)
- `pokemon_types` (associação N:N entre pokémons e tipos)

## Estrutura

```
app/        código da API (main, config, database, models, schemas, crud, routers)
tests/      testes automatizados
Dockerfile
docker-compose.yml
```
