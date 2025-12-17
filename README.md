# ativar o ambiente
. venv/Scripts/activate

# Rodar o sistema
uvicorn main:app --reload

# Criar migration
alembic revision --autogenerate -m "mensagem" = Cria a migration do banco

# Rodar migration
alembic upgrade head = executa a migration
