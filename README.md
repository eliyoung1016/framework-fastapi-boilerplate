# Framework Python with PostgreSQL

This project is configured to run with Docker Compose, including a PostgreSQL database.

## Prerequisites

- Docker and Docker Compose installed.

## Running the Application

1.  Build and start the services:

    ```bash
    docker compose up --build
    ```

2.  The application will be available at http://localhost:8000.
    ```

## Stopping the Application

To stop the services:

```bash
docker compose down
```

## Development

The `app` directory is mounted as a volume in `docker-compose.yml`, so changes to the code will be reflected immediately.

## Database Migrations (Alembic)

This project uses [Alembic](https://alembic.sqlalchemy.org/) to manage database schema migrations. For instructions on how to use Alembic to update tables, or for debugging, please see [ALEMBIC.md](docs/ALEMBIC.md).
