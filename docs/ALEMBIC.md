# Managing Database Migrations with Alembic

We use [Alembic](https://alembic.sqlalchemy.org/) to manage our PostgreSQL database schemas.

## Basic Usage

### Creating a New Migration

Whenever you update your SQLAlchemy models located in `app/models/`:
1.  Make sure your new models are imported into `app/models/__init__.py`.
2.  Generate a new migration script using the `--autogenerate` flag:

    ```bash
    uv run alembic revision --autogenerate -m "description of your changes"
    ```

3.  Review the generated script inside the `app/alembic/versions/` directory to ensure Alembic detected your changes correctly.

### Applying Migrations

To apply all pending migrations to the local database, run:

```bash
uv run alembic upgrade head
```

### Reverting Migrations

If a mistake was made, you can easily downgrade by one revision:

```bash
uv run alembic downgrade -1
```

## Debugging

### How to Clean Migrate Everything

Sometimes you may want to completely reset the database to a fresh state (WARNING: This will delete all data!). Since Alembic manages its state using the `alembic_version` table in your database, the easiest way to reset everything in our dockerized environment is to clear the PostgreSQL volume entirely.

1. Bring down the docker containers and delete the associated volumes:
   ```bash
   docker-compose down -v
   ```
2. Delete all files in your `app/alembic/versions/` folder.
3. Bring the database back up:
   ```bash
   docker-compose up -d postgres
   ```
4. Re-generate the initial migration:
   ```bash
   uv run alembic revision --autogenerate -m "initial migration"
   ```
5. Apply the migration:
   ```bash
   uv run alembic upgrade head
   ```

### Alembic Fails to Detect Changes

If Alembic does not pick up your changes when running `--autogenerate`:
- Verify that your model class is correctly inheriting from `Base`.
- Verification that your model is exported in `app/models/__init__.py`. If Alembic cannot import it within its `env.py` context, it won't see it.
