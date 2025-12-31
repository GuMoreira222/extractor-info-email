# Testes

Testes básicos para o projeto Extractor Info Email.

## Executar testes

```bash
# Executar todos os testes
poetry run pytest

# Executar com verbose
poetry run pytest -v

# Executar um arquivo específico
poetry run pytest tests/test_security.py

# Executar com cobertura
poetry run pytest --cov=app --cov-report=html
```

## Estrutura

- `test_security.py` - Testes de funções de segurança (hash, verify password, JWT)
- `test_api.py` - Testes básicos dos endpoints da API
- `test_claims.py` - Testes do endpoint de processamento de e-mails
- `conftest.py` - Configuração compartilhada (fixtures)

