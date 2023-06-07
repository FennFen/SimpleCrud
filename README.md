# FastAPI Docker Project

This is a sample FastAPI project that is containerized using Docker.

## Key Features

- Dockerized FastAPI project
- Dockerized PostgreSQL database
- Uses Repository Pattern
- Uses Dependency Injection
- Uses Pydantic for data validation
- Uses SQLAlchemy for ORM
- Uses Alembic for migrations
- Uses Pytest for testing
- Tests are done using SQLite in-memory database to avoid the hustle of creating a PostgreSQL database for testing with 3rd party libraries

## Requirements

- Docker

## Getting Started

1. Run the project:

    1. Run the containers:
      ```shell
       docker-compose up -d
      ```
    2. Run the migrations, you may need to wait for the database to be ready:
      ```shell
       docker-compose exec api bash scripts/run_migrations.sh
     ```

2. Go to http://localhost:8000/docs to view the Swagger UI.
3. Go to http://localhost:8000/redoc to view the ReDoc UI.
4. Go to http://localhost:8000 to view the API.
5. To run tests:
   ```shell
    docker-compose exec api pytest
    ```
