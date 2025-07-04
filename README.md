# Movies Agent

This project is a text-to-SQL agent built with LangGraph that uses a SQLite database of movie information.

## Setup

### 1. Install Dependencies

This project uses `uv` for package management.

```bash
uv sync
```

### 2. Initialize the Database

To set up the database for the first time, run the following commands:

1.  **Apply Database Migrations:**
    This will create the `movies.db` file and set up the necessary tables.

    ```bash
    python -m alembic upgrade head
    ```

2.  **Load Data:**
    This script will populate the database with data from the provided CSV files.

    ```bash
    python -m app.load_data
    ```

After these steps, your `movies.db` will be ready to use.
