import pytest


def test_listar_produtos_banco_vazio(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto_verifica_persistencia(client):
    payload = {"nome": "Mouse gamer", "preco": 159.9, "estoque": 5, "ativo": True}

    response = client.post("/produtos", json=payload)
    produto_id = response.json()["id"]
    persisted = client.get(f"/produtos/{produto_id}")

    assert response.status_code == 201
    assert persisted.status_code == 200
    assert persisted.json()["nome"] == payload["nome"]


def test_criar_produto_aparece_na_listagem(client):
    payload = {"nome": "Monitor LED", "preco": 899.0, "estoque": 3, "ativo": True}

    client.post("/produtos", json=payload)
    response = client.get("/produtos")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == payload["nome"]


def test_buscar_produto_por_id_sucesso(client, produto_existente):
    response = client.get(f"/produtos/{produto_existente['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == produto_existente["id"]


def test_buscar_produto_id_inexistente_retorna_404(client):
    response = client.get("/produtos/999")

    assert response.status_code == 404


def test_deletar_produto_retorna_204(client, produto_existente):
    response = client.delete(f"/produtos/{produto_existente['id']}")

    assert response.status_code == 204
    assert response.text == ""


def test_deletar_produto_confirma_remocao_com_get(client, produto_existente):
    client.delete(f"/produtos/{produto_existente['id']}")
    response = client.get(f"/produtos/{produto_existente['id']}")

    assert response.status_code == 404


def test_deletar_produto_inexistente_retorna_404(client):
    response = client.delete("/produtos/999")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "", "preco": 10.0, "estoque": 1, "ativo": True},
        {"nome": "Produto sem preço válido", "preco": 0, "estoque": 1, "ativo": True},
        {"nome": "Estoque inválido", "preco": 10.0, "estoque": -1, "ativo": True},
        {"preco": 10.0, "estoque": 1, "ativo": True},
    ],
)
def test_payloads_invalidos_retorna_422(client, payload):
    response = client.post("/produtos", json=payload)

    assert response.status_code == 422


def test_banco_isolado_entre_execucoes(client):
    response = client.get("/produtos")

    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto_com_valores_padrao(client):
    response = client.post("/produtos", json={"nome": "Cabo USB", "preco": 19.9})

    assert response.status_code == 201
    assert response.json()["estoque"] == 0
    assert response.json()["ativo"] is True
