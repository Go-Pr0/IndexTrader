# Asynchronous Processing and Reliability

## Asynchronous Task Reliability

-   **Retry Policy**: All critical Celery tasks that interact with external APIs (e.g., `execute_trade`, `reconcile_all_positions`) will be designed with a retry policy. Tasks will automatically be retried up to **3 times** with an **exponential backoff** delay (e.g., 60s, 300s, 900s) in case of transient network errors or API 5xx-level failures. Only after the final retry fails will the task be marked as permanently `FAILED`.
-   **Idempotency**: The `execute_trade` task will be made idempotent. When the API service first creates the `synthetic_positions` entry and marks it as `PENDING`, this acts as a lock. The Celery worker, before executing the trade, will first check the status of the position. If the status is anything other than `PENDING` (e.g., `EXECUTING` or `ACTIVE`), the worker will immediately discard the duplicate task, preventing re-execution.

## Trade Failure & Atomicity

The system prioritizes transparency and user control over guaranteed execution, acknowledging the potential for partial failures in a multi-leg trade.

*   **Non-Atomic Execution**: The system executes all required trades for a position in sequence. It does **not** guarantee that the entire batch of trades will succeed atomically.
*   **Execution Halting**: If any trade in the sequence fails (e.g., due to a Bybit API error, insufficient margin, or a delisted asset), the system will immediately **stop** the execution process.
*   **No Automatic Reversal**: The system will **not** attempt to reverse any trades that were successfully completed before the failure.
*   **Reconciliation as Fallback**: The partially opened position will be handled by the standard reconciliation process. The UI will flag the position as "Altered," showing the user exactly which components were successfully acquired and which are missing, allowing them to decide how to proceed.

## Position Reconciliation

The platform is designed to be tolerant of manual user intervention on their Bybit account. It will track deviations and provide tools to manage them without taking automated corrective action.

*   **P&L Calculation**: Profit and Loss will always be calculated based on the current market value of the assets the platform *originally* opened for the position. The P&L will reflect the performance of the intended index strategy, even if the user has manually altered the underlying positions.

*   **Deviation Detection & Notification**:
    *   The system will periodically reconcile the expected futures positions for a synthetic index with the actual open positions on the user's Bybit account.
    *   If a mismatch is detected (e.g., the user manually reduced a 0.1 BTC long position to 0.05), the UI will clearly flag the position as "Altered".
    *   The UI will provide details about the deviation, showing exactly which asset quantities have changed and by how much (e.g., "BTC: -0.05 | Expected: 0.1, Actual: 0.05").

*   **No Automatic Rebalancing**: The system will **never** automatically buy or sell assets to bring an altered position back into balance. The user retains full control.

*   **Manual Restore (Advanced Feature)**:
    *   Next to the "Altered" status, the UI will present an optional "Restore Balance" button. This is considered an advanced feature for a future release.
    *   When clicked, this button would trigger a confirmation modal that details the exact trades required to bring the position back to its original target allocation (e.g., "Action: Buy 0.05 BTC"). Upon confirmation, the system would execute these rebalancing trades.

*   **Closing a Position**: When a user chooses to close a position, the system's action is based on its own records, not the current state of the user's exchange account. For each asset listed in the `position_components` table for that specific position, the system will execute a **market sell order** for the **original `expected_quantity`**. All closing orders will use a **"reduce-only" parameter**. This ensures the platform only ever closes the exact position it opened, leaving any manually added positions untouched. If the user has already partially closed a position, the "reduce-only" flag ensures the order only closes the remaining amount without error. 