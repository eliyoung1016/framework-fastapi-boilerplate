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

3.  To verify the database connection, visit http://localhost:8000/db.
    You should see a JSON response with the PostgreSQL version, e.g.:
    ```json
    {"version": "PostgreSQL 18.x ..."}
    ```

## Stopping the Application

To stop the services:

```bash
docker compose down
```

## Development

The `app` directory is mounted as a volume in `docker-compose.yml`, so changes to the code will be reflected immediately (thanks to `uvicorn --reload`).

## Database Migrations (Alembic)

This project uses [Alembic](https://alembic.sqlalchemy.org/) to manage database schema migrations. For instructions on how to use Alembic to update tables, or for debugging, please see [ALEMBIC.md](ALEMBIC.md).
