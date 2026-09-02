# Sistema de Chamados — Nexa Solutions

[![Tests](https://github.com/DouglasLiebl/nexa-solutions/actions/workflows/test.yml/badge.svg)](https://github.com/DouglasLiebl/nexa-solutions/actions/workflows/test.yml)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/django-5.x-green.svg)

API REST para abertura e acompanhamento de chamados de suporte interno, com interface HTML simples para consulta e cadastro.

## Funcionalidades

- Cadastro e consulta de chamados com título, descrição e status
- Validação de título obrigatório (HTTP 400 em vez de erro interno)
- Filtro de listagem por status (`ABERTO`, `EM_ANDAMENTO`, `CONCLUIDO`)
- Indicadores consolidados por status para a coordenação
- Ambiente reproduzível com Docker e PostgreSQL
- Configurações sensíveis via variáveis de ambiente
- Suíte de testes automatizados das funcionalidades críticas

## Tecnologias

| Camada | Stack |
|---|---|
| Backend | Python 3.12+, Django 5, Django REST Framework |
| Banco local | SQLite |
| Banco Docker | PostgreSQL 16 |
| Infra | Docker, Docker Compose |
| Frontend | HTML estático |

## Estrutura do projeto

```text
nexa-solutions/
├── backend/
│   ├── chamados/          # App de chamados (models, views, testes)
│   ├── config/            # Configurações do Django
│   ├── manage.py
│   └── requirements.txt
├── docker/
│   └── entrypoint.sh      # Espera o PostgreSQL e aplica migrações
├── frontend/
│   └── index.html         # Interface simples de consulta e cadastro
├── docs/
│   ├── issues.md          # Demandas da empresa (INC-01 a INC-07)
│   └── README.md          # Contexto didático
├── .env.example           # Modelo de variáveis de ambiente
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Início rápido (Docker)

Recomendado para validar o ambiente completo com PostgreSQL:

```bash
cp .env.example .env
docker compose up --build
```

A API ficará em `http://localhost:8000/api/chamados/`.

Para rodar em segundo plano:

```bash
docker compose up --build -d
docker compose logs -f api   # acompanhar logs
docker compose down          # encerrar
```

> **Importante:** garanta que a porta `8000` esteja livre antes de subir os containers. Se outro processo estiver usando a porta, o serviço `api` pode falhar ao iniciar.

## Configuração do ambiente

Copie o arquivo de exemplo na raiz do repositório:

```bash
cp .env.example .env
```

O `.env` **não** deve ser versionado — já está no `.gitignore`. Substitua os valores de exemplo antes de usar em produção.

| Variável | Descrição | Obrigatória |
|---|---|---|
| `DJANGO_SECRET_KEY` | Chave secreta do Django | Sim |
| `DEBUG` | Modo de depuração (`True` ou `False`) | Não |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula | Não |
| `POSTGRES_DB` | Nome do banco PostgreSQL | Sim (Docker) |
| `POSTGRES_USER` | Usuário do banco | Sim (Docker) |
| `POSTGRES_PASSWORD` | Senha do banco | Sim (Docker) |
| `POSTGRES_HOST` | Host do banco (use `db` no Docker) | Sim (Docker) |
| `POSTGRES_PORT` | Porta do banco (padrão: `5432`) | Não |

### Banco de dados por ambiente

| Ambiente | Banco | Como é configurado |
|---|---|---|
| Docker Compose | PostgreSQL | Variáveis `POSTGRES_*` injetadas pelo Compose |
| Desenvolvimento local | SQLite | Usado quando `POSTGRES_HOST` não está definido |

No desenvolvimento local, o `.env` carrega apenas `DJANGO_SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS`. As credenciais PostgreSQL são lidas somente no container Docker.

## Executar localmente (desenvolvimento)

Alternativa sem Docker, usando SQLite:

```bash
cp .env.example .env
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\Activate.ps1     # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A API estará em `http://localhost:8000/api/chamados/`.

Para usar a interface HTML, abra `frontend/index.html` no navegador com a API em execução.

## Testes automatizados

A suíte é executada automaticamente no GitHub Actions a cada push e pull request para a branch `main`. Confira o status no badge acima ou em [Actions](https://github.com/DouglasLiebl/nexa-solutions/actions/workflows/test.yml).

### Localmente

```bash
cp .env.example .env
cd backend
source .venv/bin/activate
pip install -r requirements.txt
python manage.py test chamados    # app de chamados
python manage.py test             # suíte completa
```

### No Docker

```bash
docker compose exec api python manage.py test
```

### Cobertura

| Cenário | Classe de teste |
|---|---|
| Criação válida de chamado | `CadastroChamadoValidoTests` |
| Criação sem título | `CadastroChamadoSemTituloTests` |
| Filtro por status | `FiltroChamadoPorStatusTests` |
| Indicadores | `IndicadoresChamadosTests` |

## Endpoints da API

Base URL: `http://localhost:8000/api/`

### Chamados

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/chamados/` | Lista todos os chamados |
| `GET` | `/chamados/?status=ABERTO` | Filtra chamados por status |
| `POST` | `/chamados/` | Cria um novo chamado |
| `GET` | `/chamados/{id}/` | Consulta um chamado pelo ID |
| `PUT` / `PATCH` | `/chamados/{id}/` | Atualiza um chamado existente |

**Status aceitos:** `ABERTO`, `EM_ANDAMENTO`, `CONCLUIDO`.

#### Campos do chamado

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | inteiro | — | Identificador (somente leitura) |
| `titulo` | string | sim | Título do chamado |
| `descricao` | string | não | Descrição detalhada |
| `status` | string | não | Status (`ABERTO` por padrão) |
| `criado_em` | datetime | — | Data de criação (somente leitura) |
| `atualizado_em` | datetime | — | Última atualização (somente leitura) |

### Indicadores

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/indicadores/` | Totais de chamados por status |

Resposta de exemplo:

```json
{
  "total": 4,
  "abertos": 2,
  "em_andamento": 1,
  "concluidos": 1
}
```

### Exemplos com curl

Listar chamados abertos:

```bash
curl "http://localhost:8000/api/chamados/?status=ABERTO"
```

Criar chamado:

```bash
curl -X POST http://localhost:8000/api/chamados/ \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Impressora com defeito", "descricao": "Não imprime", "status": "ABERTO"}'
```

Consultar indicadores:

```bash
curl "http://localhost:8000/api/indicadores/"
```

Atualizar status de um chamado:

```bash
curl -X PATCH http://localhost:8000/api/chamados/1/ \
  -H "Content-Type: application/json" \
  -d '{"status": "CONCLUIDO"}'
```

### Respostas de erro comuns

| Situação | HTTP | Exemplo de resposta |
|---|---|---|
| Cadastro sem título | 400 | `{"titulo": ["O título é obrigatório."]}` |
| Filtro com status inválido | 400 | `{"status": "Status inválido. Valores aceitos: ABERTO, EM_ANDAMENTO, CONCLUIDO."}` |
| Chamado não encontrado | 404 | Página padrão do Django REST Framework |

## Solução de problemas

| Problema | Causa provável | Solução |
|---|---|---|
| `ImproperlyConfigured: DJANGO_SECRET_KEY` | `.env` ausente ou incompleto | `cp .env.example .env` |
| Porta 8000 em uso | Outro servidor na mesma porta | Encerre o processo ou use `docker compose down` antes de subir novamente |
| API não conecta ao banco no Docker | Container `api` fora da rede | `docker compose down && docker compose up --build` |
| Testes locais tentam usar PostgreSQL | `POSTGRES_HOST` exportado no shell | Remova a variável ou use apenas o `.env` padrão para SQLite |

## Documentação adicional

- Demandas da empresa: [`docs/issues.md`](docs/issues.md)
- Contexto didático do repositório: [`docs/README.md`](docs/README.md)
