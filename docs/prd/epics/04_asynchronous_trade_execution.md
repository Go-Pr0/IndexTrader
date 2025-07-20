# Epic 4: Asynchronous Trade Execution

## Description

This epic covers the implementation of the asynchronous trade execution workflow using Celery. The key is to decouple the user-facing API from the long-running process of executing multi-leg trades on Bybit. This ensures the UI remains responsive and the trading process is reliable, with built-in retries and clear status management.

## User Stories

-   As a User, when I initiate a trade, I want the UI to respond immediately and show me that my trade is "Executing" so I know the system has received my request.
-   As a Platform Operator, I want all trade executions to be handled by background workers so that the main API is not blocked and can handle other requests.
-   As a Developer, I want to implement a reliable, idempotent trade execution task with an automatic retry policy to handle transient API errors from the exchange.
-   As a Developer, I want the system to record every individual trade and create an immutable snapshot of the intended position composition upon successful execution.

## Technical Requirements

### Backend (Python/FastAPI)

-   **Celery Setup (`celery_app.py`, `workers/__init__.py`):**
    -   Configure Celery to use Redis as the message broker.
    -   Define Celery Beat schedules for recurring tasks.
-   **API Endpoint (`api/endpoints/positions.py`):**
    -   `POST /api/positions`:
        1.  Receives the request from the frontend (index, size, direction).
        2.  Creates a new entry in the `synthetic_positions` table with a status of `PENDING`. This acts as an idempotency lock.
        3.  Enqueues the `execute_trade_task` with the new `position_id`.
        4.  Immediately returns a `202 Accepted` response to the frontend.
-   **Trade Execution Worker (`workers/trade_executor.py`):**
    -   **`execute_trade_task(position_id)`:**
        1.  The task is bound to Celery for access to retry mechanisms.
        2.  **Idempotency Check:** Fetches the position from the DB. If status is not `PENDING`, discard the task.
        3.  Update position status to `EXECUTING`.
        4.  Call the `trading_logic.calculate_trade_composition` service from Epic 3.
        5.  For each component in the calculated composition:
            -   Execute a **1x leverage market order** on Bybit using the user's decrypted API key.
            -   **Execution Halting:** If any trade fails, stop execution immediately, update the position status to `FAILED`, and log the error. Do not attempt to reverse successful trades.
        6.  Upon successful execution of ALL trades:
            -   Record each individual fill (with `bybit_order_id`, `price`, `quantity`) in the `trades` table.
            -   Create the immutable snapshot in the `position_components` table, recording the `symbol` and `expected_quantity` for each leg.
            -   Update the final position status to `ACTIVE`.
    -   **Reliability:**
        -   Configure the task with a retry policy: **3 retries** with **exponential backoff** (60s, 300s, 900s) for transient errors (e.g., network issues, Bybit 5xx responses).
-   **Services:**
    -   The `bybit_api.py` service will be extended to include functions for placing market orders.
    -   The `security.py` service will be used to decrypt API keys just before they are needed for an API call.

## Acceptance Criteria

-   When the user initiates a trade, the API responds with `202 Accepted` and a Celery task is created.
-   The Celery worker picks up the task and updates the position status to `EXECUTING`.
-   The worker correctly executes the multi-leg trade on Bybit.
-   Upon success, the position status becomes `ACTIVE`, and the `trades` and `position_components` tables are correctly populated.
-   If a trade fails mid-execution, the process stops, and the position status is marked `FAILED`.
-   The task automatically retries on transient errors from the Bybit API.
-   The `execute_trade_task` is idempotent and will not re-execute a trade for a position that is already `EXECUTING` or `ACTIVE`. 