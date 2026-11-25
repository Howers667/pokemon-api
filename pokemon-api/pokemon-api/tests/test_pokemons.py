def test_health(client):
    assert client.get("/").json() == {"status": "ok"}


# ---------- CREATE ----------
def test_create_pokemon(client, pikachu):
    r = client.post("/pokemons", json=pikachu)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] == 1
    assert body["name"] == "pikachu"  # normalizado para minúsculas
    assert body["types"] == ["electric"]


def test_create_duplicate_returns_409(client, pikachu):
    client.post("/pokemons", json=pikachu)
    r = client.post("/pokemons", json=pikachu)
    assert r.status_code == 409


def test_create_invalid_payload_returns_422(client, pikachu):
    pikachu["hp"] = -5
    assert client.post("/pokemons", json=pikachu).status_code == 422


def test_create_without_types_returns_422(client, pikachu):
    pikachu["types"] = []
    assert client.post("/pokemons", json=pikachu).status_code == 422


def test_create_reuses_existing_type(client, pikachu):
    client.post("/pokemons", json=pikachu)
    raichu = {**pikachu, "name": "raichu"}
    assert client.post("/pokemons", json=raichu).status_code == 201


# ---------- READ ----------
def test_list_empty(client):
    r = client.get("/pokemons")
    assert r.status_code == 200
    assert r.json() == []


def test_list_pagination(client, pikachu):
    for i in range(5):
        client.post("/pokemons", json={**pikachu, "name": f"poke{i}"})
    r = client.get("/pokemons", params={"skip": 1, "limit": 2})
    assert [p["name"] for p in r.json()] == ["poke1", "poke2"]


def test_list_filter_by_type(client, pikachu):
    client.post("/pokemons", json=pikachu)
    charmander = {**pikachu, "name": "charmander", "types": ["fire"]}
    client.post("/pokemons", json=charmander)
    r = client.get("/pokemons", params={"type": "fire"})
    assert [p["name"] for p in r.json()] == ["charmander"]


def test_get_pokemon(client, pikachu):
    created = client.post("/pokemons", json=pikachu).json()
    r = client.get(f"/pokemons/{created['id']}")
    assert r.status_code == 200
    assert r.json()["name"] == "pikachu"


def test_get_not_found(client):
    assert client.get("/pokemons/999").status_code == 404


# ---------- UPDATE ----------
def test_update_partial(client, pikachu):
    pid = client.post("/pokemons", json=pikachu).json()["id"]
    r = client.patch(f"/pokemons/{pid}", json={"hp": 40, "types": ["electric", "flying"]})
    assert r.status_code == 200
    body = r.json()
    assert body["hp"] == 40
    assert body["attack"] == 55  # não alterado
    assert body["types"] == ["electric", "flying"]


def test_update_not_found(client):
    assert client.patch("/pokemons/999", json={"hp": 10}).status_code == 404


def test_update_to_duplicate_name_returns_409(client, pikachu):
    client.post("/pokemons", json=pikachu)
    other = client.post("/pokemons", json={**pikachu, "name": "raichu"}).json()
    r = client.patch(f"/pokemons/{other['id']}", json={"name": "pikachu"})
    assert r.status_code == 409


def test_update_invalid_value_returns_422(client, pikachu):
    pid = client.post("/pokemons", json=pikachu).json()["id"]
    assert client.patch(f"/pokemons/{pid}", json={"hp": 0}).status_code == 422


# ---------- DELETE ----------
def test_delete(client, pikachu):
    pid = client.post("/pokemons", json=pikachu).json()["id"]
    assert client.delete(f"/pokemons/{pid}").status_code == 204
    assert client.get(f"/pokemons/{pid}").status_code == 404


def test_delete_not_found(client):
    assert client.delete("/pokemons/999").status_code == 404
