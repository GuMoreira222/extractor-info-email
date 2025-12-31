"""Testes básicos para endpoints da API."""


def test_root_endpoint(client):
    """Testa o endpoint raiz."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Extractor Info Email API is running" in response.json()["message"]


def test_login_without_credentials(client):
    """Testa login sem credenciais."""
    response = client.post("/api/v1/login/access-token")
    assert response.status_code == 422  # Unprocessable Entity


def test_login_with_wrong_credentials(client):
    """Testa login com credenciais incorretas."""
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "wrong_user", "password": "wrong_pass"}
    )
    assert response.status_code == 401  # Unauthorized


def test_process_endpoint_without_auth(client):
    """Testa endpoint de processamento sem autenticação."""
    response = client.post(
        "/api/v1/process",
        json={"subject": "Test", "body": "Test body"}
    )
    assert response.status_code == 401  # Unauthorized


def test_process_endpoint_with_invalid_token(client):
    """Testa endpoint de processamento com token inválido."""
    response = client.post(
        "/api/v1/process",
        json={"subject": "Test", "body": "Test body"},
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 403  # Forbidden

