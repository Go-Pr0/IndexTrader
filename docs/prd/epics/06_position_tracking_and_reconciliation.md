# Epic 6: Position Tracking & Reconciliation

## Description

This epic focuses on the backend services responsible for maintaining the accuracy and integrity of user position data. It includes calculating real-time P&L, detecting deviations between the platform's records and the user's actual Bybit positions, and handling the logic for closing positions safely. The frontend work involves displaying this data clearly to the user.

## User Stories

-   As a User, I want to see the real-time Unrealized P&L for my open synthetic positions so I can track their performance.
-   As a User, if I manually change one of the underlying trades on Bybit, I want the platform to detect this and flag my position as "Altered" so I am aware of the discrepancy.
-   As a User, I want a "Close Position" button that reliably exits my synthetic position by executing the necessary reverse trades on my Bybit account.
-   As a User, I want to be confident that when I close a position, the platform only closes the trades it opened and won't touch any other positions I might have.

## Technical Requirements

### Backend (Python/FastAPI)

-   **Reconciliation Worker (`workers/position_reconciler.py`):**
    -   Create a `reconcile_all_positions` Celery task.
    -   Schedule this task to run every 5 minutes via Celery Beat (`*/5 * * * *`).
    -   **Task Logic:**
        1.  Fetch all `ACTIVE` synthetic positions from the database.
        2.  For each position, fetch the user's actual open positions from the Bybit API.
        3.  **P&L Calculation:** Calculate the Unrealized P&L based on the current market value of the assets defined in the `position_components` table (the original snapshot). Update the `unrealized_pnl` field in the `synthetic_positions` table.
        4.  **Deviation Detection:** Compare the actual quantities of assets on Bybit with the `expected_quantity` in the `position_components` table. If there is any mismatch, set the `is_altered` flag to `True` for that position.
-   **Position Closing Logic:**
    -   **API Endpoint (`api/endpoints/positions.py`):**
        -   `POST /api/positions/{position_id}/close`:
            1.  Enqueues a `close_position_task` with the `position_id`.
            2.  Returns a `202 Accepted` response.
    -   **Closing Worker (`workers/trade_closer.py`):**
        -   **`close_position_task(position_id)`:**
            1.  Fetches the position and its components from the `position_components` table.
            2.  For each component, execute a **market order** on Bybit for the reverse trade (e.g., sell what was bought).
            3.  **Crucially, all closing orders must use a "reduce-only" parameter.** This ensures the platform only ever closes the position it opened.
            4.  Upon successful closure, update the position's status to `CLOSED`.

### Frontend (Next.js)

-   **Positions Panel (`/components/dashboard/PositionsPanel.tsx`):**
    -   The P&L column should now display the `unrealized_pnl` value fetched from the backend, formatted as a currency. The color should be green for positive, red for negative.
    -   If a position's `is_altered` flag is true, display a clear "Altered" badge or icon next to its status.
    -   The "Close Position" button should trigger a confirmation modal.
    -   Upon confirmation, call the `POST /api/positions/{position_id}/close` endpoint.
    -   The UI should optimistically remove the position from the active list or show a "Closing..." state.

## Acceptance Criteria

-   The reconciliation worker runs every 5 minutes and successfully updates the P&L for all active positions.
-   The worker correctly detects when a user's position on Bybit deviates from the platform's records and sets the `is_altered` flag.
-   The dashboard UI correctly displays the real-time P&L and the "Altered" status.
-   Clicking "Close Position" successfully triggers the closing task.
-   The closing task executes the correct reverse trades using "reduce-only" orders on Bybit.
-   Successfully closed positions are removed from the user's active positions list on the dashboard. 