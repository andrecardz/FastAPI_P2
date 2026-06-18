# API de Produtos com FastAPI, Pytest e PostgreSQL

## Subir o banco de teste

```bash
docker-compose up -d db_test
```

## Executar os testes

```bash
pytest --cov=main -v
```

Também é possível rodar o comando final:

```bash
docker-compose up -d db_test && pytest --cov=main -v
```

## Saída esperada do pytest

```text
tests/test_produtos.py::test_listar_produtos_banco_vazio PASSED
tests/test_produtos.py::test_criar_produto_verifica_persistencia PASSED
tests/test_produtos.py::test_criar_produto_aparece_na_listagem PASSED
tests/test_produtos.py::test_buscar_produto_por_id_sucesso PASSED
tests/test_produtos.py::test_buscar_produto_id_inexistente_retorna_404 PASSED
tests/test_produtos.py::test_deletar_produto_retorna_204 PASSED
tests/test_produtos.py::test_deletar_produto_confirma_remocao_com_get PASSED
tests/test_produtos.py::test_deletar_produto_inexistente_retorna_404 PASSED
tests/test_produtos.py::test_payloads_invalidos_retorna_422[payload0] PASSED
tests/test_produtos.py::test_payloads_invalidos_retorna_422[payload1] PASSED
tests/test_produtos.py::test_payloads_invalidos_retorna_422[payload2] PASSED
tests/test_produtos.py::test_payloads_invalidos_retorna_422[payload3] PASSED
tests/test_produtos.py::test_banco_isolado_entre_execucoes PASSED
tests/test_produtos.py::test_criar_produto_com_valores_padrao PASSED

Name      Stmts   Miss  Cover
-----------------------------
main.py      69      5    93%
-----------------------------
TOTAL        69      5    93%

14 passed
```

## Isolamento entre testes

A fixture `client` cria as tabelas no banco PostgreSQL de teste antes de cada teste com `Base.metadata.create_all`, substitui a dependência `get_db` usando `app.dependency_overrides`, entrega o `TestClient` com `yield` e remove as tabelas no teardown com `Base.metadata.drop_all`. Assim, cada teste começa com um banco limpo e não depende do estado deixado por outros testes.
