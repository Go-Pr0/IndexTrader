# Epic 5: Frontend Dashboard & Trading Interface

## Description

This epic covers the creation of the primary user interface: the dashboard. This is where users will view index data, initiate trades, and see their open positions. The focus is on building a clean, intuitive, and responsive UI that aligns with the `frontend.md` specification, including handling optimistic updates and polling for real-time data.

## User Stories

-   As a User, I want to see a real-time chart and the current value of the BTC.D index so I can make informed trading decisions.
-   As a User, I want a simple trading panel where I can enter my desired position size in USDT and click "Buy" or "Sell" to execute a trade.
-   As a User, before my trade is executed, I want to see a confirmation modal that clearly explains the trades that will happen on my Bybit account and notifies me about trading fees.
-   As a User, I want the UI to give me immediate feedback, optimistically showing my new position as "Executing" so I have confidence the system is working.
-   As a User, I want to see my available USDT balance from my Bybit Unified Trading Account on the dashboard so I know how much capital I can deploy.

## Technical Requirements

### Frontend (Next.js)

-   **Dashboard Page (`app/dashboard/page.tsx`):**
    -   Build the main page layout with the dark theme, using the specified color palette and typography.
    -   Implement the **Navigation Bar** component.
    -   **Account Status Header:**
        -   Fetch and display the user's Bybit **Unified Trading Account USDT Balance**.
        -   Show "Bybit Account: Connected" status.
    -   **Index Trading Card:**
        -   Integrate a charting library to display the index value (mock data for now).
        -   Create the trading form with "Position Size (USDT)" input and "Buy/Sell" buttons.
        -   On button click, trigger the confirmation **Modal** component.
        -   The modal must display the estimated trades and the disclaimer about Bybit fees.
        -   Upon confirmation, call the backend `POST /api/positions` endpoint.
    -   **UI States:**
        -   Implement the loading/disabled state for the "Buy/Sell" buttons after a trade is initiated.
        -   Implement the optimistic UI update for the positions panel, showing a shimmering/loading new row.
        -   Handle success and failure cases, removing the optimistic row and showing a toast notification on failure.
-   **Positions Panel Component:**
    -   This will be a key component on the dashboard.
    -   It will display a table of active synthetic positions with columns: `Index`, `Side`, `Size (USDT)`, `Unrealized P&L`.
    -   Each row will have a "Close Position" button.
-   **Data Polling:**
    -   Implement an HTTP polling mechanism that re-fetches data from the `GET /api/positions` endpoint every **10 seconds** when the page is visible.
    -   This will be the primary way the UI gets updates on position status (`PENDING` -> `EXECUTING` -> `ACTIVE`).
    -   Implement the polling error handling (e.g., showing a "stale data" indicator).
-   **Reusable Components (`components/ui/`):**
    -   Build out the component library as specified in `frontend.md`: `Button`, `Panel/Card`, `Input`, `Table`, `Modal`, `Spinner`.

## Acceptance Criteria

-   The dashboard UI matches the design specified in `frontend.md`.
-   The user's Bybit USDT balance is correctly fetched and displayed.
-   The trading form and confirmation modal work as expected.
-   Initiating a trade triggers the correct API call and the UI enters the correct optimistic/loading state.
-   The positions panel correctly displays a list of positions fetched from the backend.
-   The 10-second polling mechanism is implemented and correctly updates the UI with new data from the backend.
-   A toast notification is shown if the trade execution ultimately fails.
-   The "Empty State" for the positions panel is shown when the user has no positions. 