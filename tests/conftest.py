"""Configuração compartilhada para testes."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db
from app.models.user import User
from app.core.security import get_password_hash

# Banco de dados em memória para testes (mais rápido, não deixa arquivos)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados para cada teste."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Cria usuário de teste
    test_user = User(
        username="test_user",
        hashed_password=get_password_hash("test_password")
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste com banco de dados mockado."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Sobrescreve get_db tanto em app.db.session quanto em app.api.deps
    from app.api import deps as api_deps
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[api_deps.get_db] = override_get_db
    
    yield TestClient(app)
    
    # Limpa as sobrescritas após o teste
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client, db_session):
    """Retorna um token de autenticação válido."""
    # Verifica se o usuário existe no banco
    user = db_session.query(User).filter(User.username == "test_user").first()
    assert user is not None, "Usuário de teste não foi criado"
    
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "test_user", "password": "test_password"}
    )
    
    if response.status_code != 200:
        print(f"Erro no login: {response.status_code}")
        print(f"Resposta: {response.text}")
    
    assert response.status_code == 200, f"Login falhou: {response.text}"
    return response.json()["access_token"]

