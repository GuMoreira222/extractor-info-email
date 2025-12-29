# Extractor Info Email

API REST desenvolvida em FastAPI para extração automatizada de informações estruturadas de e-mails de sinistros de seguros utilizando inteligência artificial (Groq AI).

## 📋 Sobre o Projeto

O **Extractor Info Email** é uma solução que processa e-mails de clientes relacionados a sinistros de seguros e extrai automaticamente informações estruturadas como tipo de sinistro, local do evento, nível de urgência, dados faltantes, entre outros. Utiliza o modelo LLM da Groq para realizar a extração de dados de forma inteligente.

## ✨ Funcionalidades

- 🔐 Autenticação JWT (Bearer Token)
- 📧 Processamento de e-mails de sinistros
- 🤖 Extração automática de dados usando IA (Groq)
- 📊 Retorno estruturado em JSON
- 🐳 Containerização com Docker
- ☁️ Pronto para deploy em Azure Container Apps (ACA)

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Python 3.13** - Linguagem de programação
- **SQLAlchemy** - ORM para banco de dados
- **Groq AI** - Modelo LLM para extração de informações
- **LangChain** - Framework para aplicações LLM
- **Poetry** - Gerenciamento de dependências
- **PostgreSQL** - Banco de dados (via psycopg2)
- **Docker** - Containerização

## 📦 Requisitos

- Python >= 3.13
- Poetry
- PostgreSQL (ou outro banco de dados suportado pelo SQLAlchemy)
- Conta na Groq com API Key

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd extractor-info-email
```

### 2. Instale as dependências com Poetry

```bash
poetry install
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta_aqui
SQLALCHEMY_DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
GROQ_API_KEY=sua_groq_api_key_aqui
API_USER=seu_usuario
API_PASSWORD=sua_senha
```

### 4. Inicialize o banco de dados

```bash
poetry run python app/db/init_db.py
```

Isso criará as tabelas necessárias e um usuário admin padrão:
- **Username:** `admin`
- **Password:** `admin`

## 🏃 Como Executar

### Desenvolvimento Local

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

### Documentação Interativa

Acesse a documentação interativa da API:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🐳 Docker

### Build da imagem

```bash
docker build -t extractor-info-email .
```

### Executar container

```bash
docker run -p 8080:8080 --env-file .env extractor-info-email
```

## 📡 Endpoints da API

### Autenticação

#### POST `/api/v1/login/access-token`

Realiza login e retorna token de acesso.

**Body (form-data):**
```
username: admin
password: admin
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Processamento de E-mails

#### POST `/api/v1/process`

Processa um e-mail de sinistro e extrai informações estruturadas.

**Headers:**
```
Authorization: Bearer <seu_token>
Content-Type: application/json
```

**Body:**
```json
{
  "subject": "Sinistro de automóvel - batida",
  "body": "Olá, tive um acidente hoje de manhã na Avenida Paulista. Meu carro foi atingido por outro veículo. Preciso de ajuda urgente!"
}
```

**Resposta:**
```json
{
  "tipo_sinistro": "automovel",
  "resumo": "Cliente teve acidente de trânsito na Avenida Paulista",
  "data_ocorrido": "2024-01-15",
  "placa_veiculo": null,
  "local_evento": "Avenida Paulista",
  "nivel_urgencia": "Alta",
  "informacoes_faltantes": ["placa_veiculo", "numero_apolice"]
}
```

## 📁 Estrutura do Projeto

```
extractor-info-email/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependências (autenticação, DB)
│   │   └── v1/
│   │       ├── api.py            # Router principal
│   │       └── endpoints/
│   │           ├── auth.py      # Endpoints de autenticação
│   │           └── claims.py    # Endpoints de processamento
│   ├── core/
│   │   ├── config.py            # Configurações (Settings)
│   │   └── security.py          # Funções de segurança (hash, JWT)
│   ├── db/
│   │   ├── session.py           # Configuração do banco de dados
│   │   └── init_db.py           # Inicialização do banco
│   ├── models/
│   │   └── user.py              # Modelo de usuário
│   ├── schemas/
│   │   ├── claim.py             # Schemas de sinistro
│   │   ├── token.py             # Schemas de token
│   │   └── user.py              # Schemas de usuário
│   ├── services/
│   │   └── groq_service.py      # Serviço de integração com Groq
│   └── main.py                  # Aplicação FastAPI
├── data/
│   └── database.db              # Banco de dados SQLite (desenvolvimento)
├── Dockerfile
├── .dockerignore
├── pyproject.toml
├── poetry.lock
└── README.md
```

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|------------|
| `SECRET_KEY` | Chave secreta para JWT | Sim |
| `SQLALCHEMY_DATABASE_URL` | URL de conexão do banco de dados | Sim |
| `GROQ_API_KEY` | API Key da Groq | Sim |
| `API_USER` | Usuário da API | Sim |
| `API_PASSWORD` | Senha da API | Sim |

### Modelo Groq

O projeto utiliza o modelo `llama-3.3-70b-versatile` da Groq. Para alterar o modelo, edite o arquivo `app/services/groq_service.py`.

## 🧪 Exemplos de Uso

### Usando cURL

#### 1. Fazer login

```bash
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"
```

#### 2. Processar e-mail

```bash
curl -X POST "http://localhost:8000/api/v1/process" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Sinistro de automóvel",
    "body": "Tive um acidente hoje na Avenida Paulista"
  }'
```

### Usando Python

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/login/access-token",
    data={"username": "admin", "password": "admin"}
)
token = response.json()["access_token"]

# Processar e-mail
headers = {"Authorization": f"Bearer {token}"}
data = {
    "subject": "Sinistro de automóvel",
    "body": "Tive um acidente hoje na Avenida Paulista"
}
response = requests.post(
    "http://localhost:8000/api/v1/process",
    headers=headers,
    json=data
)
print(response.json())
```

## ☁️ Deploy no Azure Container Apps

1. Build e push da imagem para Azure Container Registry
2. Configure as variáveis de ambiente no Azure Container App
3. Configure a porta do container para `8080`
4. Configure o Ingress para aceitar tráfego externo

## 📝 Licença

Este projeto está sob a licença especificada no arquivo `LICENSE`.

## 👤 Autor

**gustavo**

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

Desenvolvido com ❤️ usando FastAPI e Groq AI
