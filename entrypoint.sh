#!/bin/sh

# Executa as migrações da base de dados
poetry run alembic upgrade head

# Inicia a aplicação FastAPI
poetry run uvicorn fast_zero.app:app --host 0.0.0.0 --port 8000
