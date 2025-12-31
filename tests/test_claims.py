"""Testes básicos para endpoint de processamento de e-mails."""
from unittest.mock import patch, MagicMock
from app.schemas.claim import ClaimExtraction, ClaimType


@patch("app.services.groq_service.ChatGroq")
def test_process_email_success(mock_groq, client, auth_token):
    """Testa processamento de e-mail com sucesso."""
    # Mock do Groq Service
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    
    mock_result = ClaimExtraction(
        tipo_sinistro=ClaimType.AUTO,
        resumo="Teste de sinistro de automóvel",
        data_ocorrido="2024-01-15",
        placa_veiculo=None,
        local_evento="Avenida Paulista",
        nivel_urgencia="Alta",
        informacoes_faltantes=["numero_apolice"]
    )
    
    mock_structured_llm.invoke.return_value = mock_result
    mock_llm.with_structured_output.return_value = mock_structured_llm
    mock_groq.return_value = mock_llm
    
    response = client.post(
        "/api/v1/process",
        json={
            "subject": "Sinistro de automóvel",
            "body": "Tive um acidente hoje na Avenida Paulista"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "tipo_sinistro" in data
    assert data["tipo_sinistro"] == "automovel"
    assert "resumo" in data
    assert "nivel_urgencia" in data


def test_process_email_invalid_request(client, auth_token):
    """Testa processamento com dados inválidos."""
    response = client.post(
        "/api/v1/process",
        json={"subject": ""},  # Body faltando
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 422  # Unprocessable Entity

