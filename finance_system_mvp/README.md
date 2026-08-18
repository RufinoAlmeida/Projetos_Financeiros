# Finance System — MVP

MVP do sistema de controle de receitas e despesas baseado na especificação enviada.

## Implementado

- FastAPI
- SQLAlchemy 2
- PostgreSQL via Docker
- SQLite para execução local simples
- JWT
- Hash de senha
- Usuários
- Categorias
- Contas bancárias
- Receitas e despesas
- Dashboard via API
- Validação Pydantic
- Separação em models, schemas, services, repositories e routes
- CORS
- Docker Compose
- Swagger/OpenAPI

A especificação original define FastAPI, PostgreSQL, SQLAlchemy, Alembic, React/TypeScript/TailwindCSS e JWT. Este MVP implementa primeiro o backend e deixa a expansão dos módulos avançados para as próximas etapas. fileciteturn0file0L38-L78

## Estrutura

backend/
  app/
    api/
    core/
    database/
    models/
    repositories/
    schemas/
    services/

## Rodar localmente

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Linux/macOS:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger:
http://127.0.0.1:8000/docs

## Rodar com PostgreSQL

Na raiz:

```bash
docker compose up --build
```

Swagger:
http://127.0.0.1:8000/docs

## Primeiro teste da API

1. POST `/api/auth/register`
2. POST `/api/auth/login`
3. Copie `access_token`
4. Clique em Authorize no Swagger e informe `Bearer <token>`
5. Crie uma categoria
6. Crie uma conta
7. Cadastre receitas e despesas
8. Consulte `/api/transactions/dashboard`

## Próximas fases

- React + TypeScript + Tailwind
- Dashboard visual
- CRUD completo com edição
- Contas a pagar/receber
- Cartões
- Parcelamentos
- Recorrências
- Orçamentos
- Relatórios CSV/Excel/PDF
- Auditoria
- Alembic migrations
- Testes unitários e integração
- Rate limiting
- Recuperação de senha
