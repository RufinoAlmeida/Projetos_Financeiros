# Teste PicPay Simplificado — Python

Esse projeto é baseado no teste de backend da empresa PicPay. Backend REST para o desafio de processo seletivo, implementado com **Python + FastAPI + PostgreSQL + SQLAlchemy + Docker + Pytest + GitHub Actions**.

## Objetivos

A implementação cobre as regras centrais do desafio:

* Usuários comuns e lojistas.
* CPF/CNPJ e e-mail únicos.
* Carteira por usuário.
* Usuário comum pode transferir.
* Lojista apenas recebe.
* Validação de saldo.
* Autorização em serviço externo via GET.
* Transferência atômica com transação de banco.
* Registro da transferência.
* Notificação desacoplada por **Transactional Outbox**.
* Tratamento de erros de negócio.
* Testes unitários.
* Docker para execução reproduzível.

## Arquitetura

```text
HTTP
  ↓
FastAPI Controller
  ↓
Application Service
  ↓
Repositories / SQLAlchemy
  ↓
PostgreSQL

External integrations:
TransferService → AuthorizationGateway → HTTP service
TransferService → Outbox → NotificationGateway → HTTP service
```

A regra financeira fica no `TransferService`; integrações externas ficam atrás de gateways. Isso reduz acoplamento e facilita testes.

## Por que Transactional Outbox?

A transferência financeira não deve ser desfeita somente porque o serviço de notificação está indisponível. Por isso, a transferência e o evento `transfer.completed` são persistidos na mesma transação. Depois do commit, a notificação é processada em background.

Se a notificação falhar, o evento permanece como `failed` e pode ser reprocessado sem alterar o saldo da carteira.

## Concorrência

As carteiras são carregadas com `SELECT ... FOR UPDATE` em bancos que suportam row-level locking, evitando que duas transferências concorrentes gastem o mesmo saldo. O PostgreSQL é o banco de produção recomendado para esse comportamento.

## Endpoints

### Health

`GET /health`

### Criar usuário

`POST /users`

```json
{
  "name": "Zeze",
  "document": "12345678909",
  "email": "zeze@example.com",
  "password": "Senha@123",
  "user\\\_type": "common"
}
```

### Consultar carteira

`GET /wallets/{user\\\_id}`

### Depósito de demonstração

`POST /wallets/{user\\\_id}/deposit`

Este endpoint existe apenas para facilitar o teste do desafio e deve ser removido/substituído por um fluxo financeiro autorizado em produção.

### Transferência

`POST /transfer`

```json
{
  "value": 100.00,
  "payer": 4,
  "payee": 15
}
```

Resposta:

```json
{
  "id": 1,
  "status": "completed",
  "value": 100.00,
  "payer": 4,
  "payee": 15,
  "notification": "queued"
}
```

## Executando com Docker

```bash
docker compose up --build
```

Swagger:

`http://localhost:8000/docs`

## Executando localmente

Crie um ambiente virtual e instale:

```bash
pip install -e '.\\\[dev]'
```

Defina `DATABASE\\\_URL` ou use o SQLite padrão para desenvolvimento/testes simples.

Inicialize o banco:

```bash
python -m app.infrastructure.database.init\\\_db
```

Execute:

```bash
uvicorn app.main:app --reload
```

## Testes

```bash
pytest -q
```

## Qualidade

```bash
ruff check .
pyright
pytest --cov=app --cov-report=term-missing
```

## CI

O workflow em `.github/workflows/ci.yml` executa lint, análise estática e testes.

## Decisões e trade-offs

1. **Monólito modular:** o domínio é pequeno; microsserviços aumentariam complexidade sem benefício proporcional.
2. **PostgreSQL:** adequado para consistência transacional e concorrência financeira.
3. **Decimal/Numeric:** valores monetários não usam `float`.
4. **Authorization antes da transação:** evita manter locks de banco enquanto uma chamada externa está pendente.
5. **Outbox para notificação:** evita acoplamento entre sucesso financeiro e disponibilidade do provedor de notificação.
6. **Cache não é usado para saldo:** consistência financeira é prioritária.
7. **Hash Argon2:** senha nunca é armazenada em texto puro.

## Próximas evoluções

* Idempotency-Key para evitar transferência duplicada em retries do cliente.
* Autenticação/autorização real.
* Worker dedicado para outbox com retry/backoff.
* Métricas e tracing com OpenTelemetry.
* Redis para cache de dados não financeiros.
* Mensageria dedicada (RabbitMQ/Kafka) em maior escala.
* Ledger contábil imutável para auditoria financeira.

## Explicação Técnica dos arquivos

APP > API > HEALTH.PY

Esse arquivo health.py implementa um Health check na API. 
Sua funcionalidade: Ele permite verificar rapidamente se a aplicação está respondendo.

## O que é API Router?
É um mecanismo do FastAPI para organizar as rotas da aplicação em módulos separados.

<img width="906" height="25" alt="image" src="https://github.com/user-attachments/assets/17787136-9d4a-4a0a-ad62-ae8733c4bfee" />

Aqui estamos importando APIRouter do FastAPI

## Criação do Router

<img width="879" height="32" alt="image" src="https://github.com/user-attachments/assets/746a41f0-fc4d-4c33-ab9b-10a6cd6e3af2" />

Aqui criamos uma instância de APIRouter, um conjunto de endpoints relacionados. Nesse caso, o router contém endpoints relacionados à saúde da aplicação

O que significa tags health

<img width="406" height="32" alt="image" src="https://github.com/user-attachments/assets/7c2df39d-9bdd-44ee-9cc2-e3197a4df3c0" />

É uma categoria/titulo utilizado principalmente para organização da documentação automática do FastAPI.
