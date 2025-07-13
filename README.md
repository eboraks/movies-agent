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

## 3. Running the LangGraph Server

This application can be run as a LangGraph server, which provides a web interface for interacting with the agent.

The server is configured using the `langgraph.json` file, which defines the agent to be served.

To start the server, run the following command from the root of the project:

```bash
langgraph dev
```

This will start a local development server, and you can access the LangGraph UI in your browser to send messages to the agent.

## 4. Logging runs into the LangSmith service

See: https://docs.smith.langchain.com/ for more information and instruction on how to create an account and get an API key.

To long runs into the LangSmith service, run the following environment variables needs to be set: 

```bash
LANGSMITH_API_KEY=KEY
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=movies-agent
```

 

## 5. Running the LangChain Agent UI

The LangChain Agent UI is a web interface for interacting with the agent.

Install the LangChain Agent UI from [here](https://github.com/langchain-ai/agent-chat-ui).

Run the LangChain Agent UI with the following command from the home directory:

Note: make sure to add the langsmith API key to the .env file.

```bash
pnpm dev
```

## 6. Running the LangSmith Test Dataset

To run the LangSmith test dataset, run the following command from the root of the project:

```bash
