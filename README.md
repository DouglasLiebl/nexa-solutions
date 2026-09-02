# Sistema de Chamados — Nexa Solutions

API REST para abertura e acompanhamento de chamados de suporte interno, com interface HTML simples para consulta e cadastro.

## Contexto

A Nexa Solutions utiliza este sistema para registrar chamados com título, descrição e status. O backend foi desenvolvido com Django e Django REST Framework; o frontend é uma página HTML estática que consome a API.

## Tecnologias

- Python 3.12+
- Django 5
- Django REST Framework
- SQLite (desenvolvimento local)
- PostgreSQL (ambiente Docker)
- Docker e Docker Compose
- Git

## Estrutura do projeto

```text
nexa-solutions/
├── backend/           # API Django
│   ├── chamados/      # App de chamados
│   ├── config/        # Configurações do projeto
│   ├── manage.py
│   └── requirements.txt
├── frontend/          # Interface HTML simples
│   └── index.html
├── docs/              # Documentação e demandas da empresa
├── .env.example       # Modelo de variáveis de ambiente
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pré-requisitos

Para execução local:

- Python 3.12 ou superior
- `pip` e ambiente virtual (`venv`)

Para execução com Docker:

- Docker
- Docker Compose

## Configuração do ambiente

Copie o arquivo de exemplo e ajuste os valores conforme necessário:

```bash
cp .env.example .env
```

O arquivo `.env` **não** deve ser versionado — ele já está listado no `.gitignore`. Use o `.env.example` apenas como referência, substituindo os valores de exemplo antes de subir o ambiente.

Variáveis disponíveis:

| Variável | Descrição |
|---|---|
| `DJANGO_SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | Modo de depuração (`True` ou `False`) |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula |
| `POSTGRES_DB` | Nome do banco PostgreSQL |
| `POSTGRES_USER` | Usuário do banco |
| `POSTGRES_PASSWORD` | Senha do banco |
| `POSTGRES_HOST` | Host do banco (ex.: `db` no Docker) |
| `POSTGRES_PORT` | Porta do banco (padrão: `5432`) |

## Executar com Docker

Na raiz do repositório, com o `.env` configurado:

```bash
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000/api/chamados/
```

Para encerrar os containers:

```bash
docker compose down
```

## Executar localmente (desenvolvimento)

Alternativa para desenvolvimento sem Docker:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A API estará em `http://localhost:8000/api/chamados/`.

Para usar a interface HTML, abra `frontend/index.html` no navegador com a API em execução.

## Testes automatizados

Antes de executar os testes localmente, configure o ambiente:

```bash
cp .env.example .env
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

Com o ambiente virtual ativado, execute a suíte do app de chamados:

```bash
cd backend
python manage.py test chamados
```

Para executar toda a suíte de testes do projeto:

```bash
cd backend
python manage.py test
```

A suíte cobre as funcionalidades críticas da API:

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

### Indicadores

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/indicadores/` | Totais de chamados por status |

Retorno de exemplo:

```json
{
  "total": 4,
  "abertos": 2,
  "em_andamento": 1,
  "concluidos": 1
}
```

### Exemplos

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

Cadastro sem título retorna HTTP 400 com a mensagem de validação. Status inválido no filtro também retorna HTTP 400.

### Campos do chamado

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | inteiro | — | Identificador (somente leitura) |
| `titulo` | string | sim | Título do chamado |
| `descricao` | string | não | Descrição detalhada |
| `status` | string | não | Status (`ABERTO` por padrão) |
| `criado_em` | datetime | — | Data de criação (somente leitura) |
| `atualizado_em` | datetime | — | Última atualização (somente leitura) |

## Documentação adicional

- Demandas da empresa: [`docs/issues.md`](docs/issues.md)
- Contexto didático do repositório: [`docs/README.md`](docs/README.md)
