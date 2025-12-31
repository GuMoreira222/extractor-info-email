"""Testes básicos para funções de segurança."""
from app.core import security


def test_get_password_hash():
    """Testa se a função gera um hash diferente da senha original."""
    password = "test_password_123"
    hashed = security.get_password_hash(password)
    
    assert hashed != password
    assert len(hashed) > 0
    assert isinstance(hashed, str)


def test_verify_password_correct():
    """Testa se a verificação de senha funciona com senha correta."""
    password = "test_password_123"
    hashed = security.get_password_hash(password)
    
    assert security.verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Testa se a verificação de senha funciona com senha incorreta."""
    password = "test_password_123"
    wrong_password = "wrong_password"
    hashed = security.get_password_hash(password)
    
    assert security.verify_password(wrong_password, hashed) is False


def test_create_access_token():
    """Testa se o token JWT é criado corretamente."""
    subject = "test_user_id"
    token = security.create_access_token(subject)
    
    assert isinstance(token, str)
    assert len(token) > 0
    # Token JWT tem 3 partes separadas por ponto
    assert len(token.split(".")) == 3

