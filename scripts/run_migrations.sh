cd /app/app || echo "Error: No such directory"
alembic upgrade head || echo "Error: Alembic upgrade failed"
