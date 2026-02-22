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

## Email Configuration

To enable the application to send real emails (like the test email endpoint or password resets), you must configure your SMTP settings. 

You can set these values by creating a `.env` file in the root directory and Docker Compose will automatically pick them up:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_TLS=True
EMAILS_FROM_EMAIL=your_email@gmail.com
EMAILS_FROM_NAME="My App"
```

If these are not set, the application will fallback to printing the email content to the console.

## Stopping the Application

To stop the services:

```bash
docker compose down
```

## Development

The `app` directory is mounted as a volume in `docker-compose.yml`, so changes to the code will be reflected immediately.

## Database Migrations (Alembic)

This project uses [Alembic](https://alembic.sqlalchemy.org/) to manage database schema migrations. For instructions on how to use Alembic to update tables, or for debugging, please see [ALEMBIC.md](docs/ALEMBIC.md).
