# Gerenciador de Tarefas - Ciclo de Deploy

Projeto acadêmico desenvolvido para demonstrar o ciclo de desenvolvimento, versionamento, containerização e deploy de uma aplicação web.

## Tecnologias

- Python
- Flask
- PostgreSQL
- Docker
- GitHub
- GitHub Actions
- Azure Container Registry (ACR)
- Azure Web App for Containers

## Executar localmente com Docker

Pré-requisito: Docker Desktop instalado.

```bash
docker compose up --build
```

Depois acesse:

```text
http://localhost:8000
```

## Variáveis de ambiente

A aplicação utiliza:

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD
- PORT

## Pipeline

O workflow `.github/workflows/deploy.yml` é executado quando há um `push` na branch `main`.

Fluxo:

GitHub → GitHub Actions → Docker Build → ACR → Azure Web App → PostgreSQL

## Secrets necessários no GitHub

Configure no repositório:

- AZURE_CREDENTIALS
- ACR_NAME
- RESOURCE_GROUP
- WEBAPP_NAME

As credenciais não devem ser colocadas diretamente no código.
