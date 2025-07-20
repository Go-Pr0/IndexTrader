# Backend Architecture

The backend will be a modular monolith. This approach provides development simplicity for the MVP while still separating concerns into distinct logical modules.

## Key Workflows

-   **Executing a Trade (Asynchronous)**:
    1.  User clicks "Buy Index" on the frontend.
    2.  Frontend sends a request to the `/api/positions` endpoint.
    3.  The **API Service** validates the request, creates a new entry in the `synthetic_positions` table with a status of `PENDING`, and enqueues a `execute_trade` task with the `position_id`.
    4.  The API Service immediately returns a `202 Accepted` response to the frontend with the `position_id`.
    5.  A **Celery Worker** picks up the `execute_trade` task, updates the position status to `EXECUTING`, and performs the entire multi-leg trading logic with the Bybit API.
    6.  Upon completion (or failure), the worker updates the final status of the position in the database (`ACTIVE` or `FAILED`).

-   **Updating Position P&L (Scheduled)**:
    - **Celery Beat** will enqueue a `reconcile_all_positions` task based on a cron schedule of `*/5 * * * *` (every 5 minutes).
    - A **Celery Worker** picks up this task. It queries all active positions and, for each one, fetches the latest data from Bybit, calculates P&L, checks for deviations, and updates the `synthetic_positions` table in the database.

## Configuration Management

The backend service will use Pydantic's Settings Management for robust configuration handling. All configuration values (e.g., Database URLs, API endpoints) will be loaded from environment variables. For local development, these variables will be sourced from a `.env` file, which will be included in the project's `.gitignore`. In the production environment on Render, these will be set as secure environment variables in the service's configuration.

The system will be designed to operate in both **Mainnet** and **Testnet** environments. The Bybit API base URL will be managed via an environment variable to allow developers to conduct extensive, safe testing using the Bybit Testnet without risking real funds. 