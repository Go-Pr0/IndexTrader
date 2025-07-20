# Epic 1: Project Setup & Foundational Backend

## Description

This epic covers the initial setup of the backend infrastructure. The goal is to establish a solid foundation for all subsequent development, including the FastAPI application, database connections, containerization with Docker, and configuration management. This foundational work ensures that the development environment is consistent, secure, and ready for feature implementation.

## User Stories

-   As a Developer, I want to set up a FastAPI application with a modular structure so that we can build a maintainable and scalable backend.
-   As a Developer, I want to configure two separate PostgreSQL databases (User Data & General Data) with Alembic for migrations so that we can manage database schemas systematically and ensure data isolation.
-   As a Developer, I want to create a Dockerfile for the backend so that we can have a consistent and reproducible environment for development and deployment.
-   As a Developer, I want to implement Pydantic settings management so that we can handle configuration securely and flexibly for different environments (e.g., Mainnet, Testnet).
-   As a Developer, I want to set up the basic project structure with a modular monolith approach so that concerns are logically separated from the start.

## Technical Requirements

### Backend (Python/FastAPI)

-   Initialize a new FastAPI project.
-   Structure the application into modules: `api`, `core`, `db`, `services`, `workers`.
-   **Configuration (`core/config.py`):**
    -   Use Pydantic's `BaseSettings` to manage environment variables.
    -   Include settings for:
        -   `DATABASE_URL_USER`
        -   `DATABASE_URL_GENERAL`
        -   `BYBIT_API_URL` (configurable for Mainnet/Testnet)
        -   `RENDER_MASTER_KEY_PATH` (path to the secret file)
-   **Database (`db/session.py`):**
    -   Use SQLAlchemy 2.0.
    -   Set up engine and session management for two separate databases.
    -   Initialize Alembic for managing database migrations for both databases.
-   **Containerization (`Dockerfile`):**
    -   Create a multi-stage Dockerfile to build an optimized production image.
    -   Ensure it correctly installs Python dependencies from `requirements.txt`.
-   **Dependencies (`requirements.txt`):**
    -   Include `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `alembic`, `pydantic`.

### Infrastructure (Render)

-   Define the initial `render.yaml` structure.
-   Plan for:
    -   A **Web Service** for the FastAPI API.
    -   Two **PostgreSQL** instances.
    -   A **Redis** instance.
    -   A **Background Worker** for Celery.
    -   A **Secret File** for the master encryption key.

## Acceptance Criteria

-   The FastAPI application runs successfully in a Docker container.
-   The application can connect to both PostgreSQL databases.
-   Alembic is configured and an initial migration can be generated for each database.
-   Configuration is successfully loaded from environment variables (or a `.env` file for local development).
-   The basic file structure is in place according to the architecture diagram. 