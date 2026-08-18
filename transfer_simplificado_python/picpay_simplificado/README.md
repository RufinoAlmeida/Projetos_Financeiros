# PicPay Simplificado — Python

Backend REST para o desafio de processo seletivo, implementado com **Python + FastAPI + PostgreSQL + SQLAlchemy + Docker + Pytest + GitHub Actions**.

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

