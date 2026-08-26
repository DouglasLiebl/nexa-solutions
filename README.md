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
