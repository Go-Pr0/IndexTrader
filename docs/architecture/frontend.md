# Front-End Specification: Non-Custodial Index Trading Platform

## 1. Overview and Core UX Goals

This document outlines the UI and UX for the Non-Custodial Index Trading Platform. The objective is to provide a clean, secure, and simple interface for users to execute and monitor synthetic index trades on their own Bybit accounts.

The UI will be a modern web application with a professional, minimalist aesthetic, using a **predominantly dark theme** with mint green accents to create a feeling of control and clarity.

### Core UX Goals:

1.  **Effortless Onboarding**: A new user must be able to sign up, connect their Bybit API key, and understand how to execute a trade in under five minutes.
2.  **Trust Through Transparency**: The UI must be exceptionally clear about what actions it will take on the user's behalf. Users should see estimated trade details before execution and have a clear, real-time view of their synthetic positions afterward.
3.  **Simplicity**: Abstract away the complexity of the underlying trades. The user experience should be as simple as clicking "Buy" or "Sell" on an index.

## 2. Design System & Style Guide

### Color Palette (Dark Theme)

| Role              | Color       | HEX Code  | Usage                                         |
| ----------------- | ----------- | --------- | --------------------------------------------- |
| **Primary**       | Mint Green  | `#A8E6CF` | Buttons, highlights, positive P/L, buy-side   |
| **Primary Alt**   | Bright Red  | `#F56565` | Destructive actions, negative P/L, sell-side|
| **Background**    | Near Black  | `#1A202C` | Main application background                   |
| **Surface**       | Dark Slate  | `#2D3748` | Card backgrounds, panels, modules             |
| **Primary Text**  | Off-White   | `#F7FAFC` | Headings, primary body text                   |
| **Secondary Text**| Medium Gray | `#A0AEC0` | Subtitles, labels, disabled text              |
| **Borders**       | Gray        | `#4A5568` | Input borders, panel outlines, table rows     |

### Typography

-   **Font Family**: `Inter`
-   **Key Numbers (Prices, P/L)**: `Roboto Mono`

## 3. Information Architecture & User Flows

### Site Map

-   `/` (Landing Page): Public marketing and login page.
-   `/dashboard`: The main user dashboard for viewing indices and managing positions.
-   `/settings`: Page for managing Bybit API keys.
-   `/auth/...`: Routes for handling authentication flows.

### Core User Flow: First Trade

1.  User lands on `/`, signs up, and logs in.
2.  Is redirected to the `/dashboard`, which shows a prompt to "Connect Your Exchange".
3.  User navigates to `/settings`.
4.  Follows instructions to generate a **Contract trading-enabled** API key on Bybit.
5.  Enters the API Key and Secret into the secure form and saves. The system validates the key.
6.  User returns to the `/dashboard`. The prompt is gone, and the trading panels are active.
7.  In the "BTC.D Index" panel, the user enters `1000` USDT and clicks "Buy".
8.  A confirmation modal appears, showing the approximate **futures contracts** that will be bought and sold on their Bybit account. **The modal will also include a clear disclaimer: "Standard Bybit trading fees will apply and will be deducted from your Bybit account upon execution."**
9.  User confirms. The system executes the trades via the API.
10. The "Positions" panel updates to show a new "Long BTC.D" position with a real-time P&L display based on their **open futures positions**.

## 4. Page-by-Page Breakdown

### 4.1. Dashboard (`/dashboard`)

-   **Purpose**: The main hub for viewing market indices and managing synthetic positions tied to the user's Bybit account.
-   **Key Components**:
    -   **Navigation Bar**: Logo, links to "Dashboard" and "Settings", and a User/Logout dropdown.
    -   **Account Status**: A small header display showing "Bybit Account: Connected" and the available **Unified Trading Account USDT Balance**, fetched via API.
    -   **Index Trading Card (One for each supported index, e.g., BTC.D)**:
        -   Title: "Bitcoin Dominance (BTC.D)".
        -   A real-time chart showing the index value.
        -   A simple form with an input for "Position Size (USDT)" and two buttons: "Buy (Long)" and "Sell (Short)".
    -   **Positions Panel**: A table listing all active synthetic positions.
        -   Columns: `Index`, `Side (Long/Short)`, `Size (USDT)`, `Unrealized P&L`.
        -   Each row has a "Close Position" button. Clicking it will trigger a confirmation modal that clearly states the platform will only close the quantities it originally opened, leaving any manually added positions untouched.

    **In-Flight UI States**:
       1.  **Initiation**: When the user confirms a trade in the modal, the "Buy/Sell" button in the Index Trading Card will immediately enter a disabled, loading state to prevent duplicate clicks.
       2.  **Optimistic Update**: A new row will optimistically appear in the "Positions Panel" with a grayed-out or shimmering loading effect, showing the intended position size and an "Executing..." status.
       3.  **Success**: Upon successful execution of all trades, the row in the "Positions Panel" will transition to its normal, "Active" state, and the P&L calculation will begin. The "Buy/Sell" button will become active again.
       4.  If any part of the trade execution fails, the optimistic row in the "Positions Panel" will be removed, and a user-friendly toast notification will appear at the top of the screen with a clear error message (e.g., "Trade Failed: Insufficient balance on Bybit."). The "Buy/Sell" button will become active again.

    **Data Refresh and Real-Time Updates**:
        *   To keep dashboard data current, the frontend will employ an HTTP polling strategy.
        *   When the `/dashboard` page is active and visible to the user, the application will automatically re-fetch all position data from a dedicated backend endpoint (e.g., `GET /api/positions`) every **10 seconds**. This polling is the primary mechanism for receiving updates on position status (e.g., transitioning from `EXECUTING` to `ACTIVE`), P&L, and alterations.
        *   **Polling Error Handling**: If an API poll fails to receive a successful response from the backend, a small, non-intrusive indicator will appear on the dashboard (e.g., a yellow or red dot next to the 'Bybit Account: Connected' status). The UI will continue to display the last known data but will clearly indicate that the data is stale. The polling will continue in the background, and the indicator will disappear once a successful connection is re-established.
        *   This provides a near-real-time experience for the user without the complexity of a WebSocket implementation, which is suitable for the MVP.

    **Empty State**: When a user has connected their API key but has no open synthetic positions, the "Positions Panel" will display a clear, centered message: *"You have no open positions. Use the panel above to buy or sell an index to get started."* This provides a helpful call to action.

### 4.2. Settings (`/settings`)

-   **Purpose**: To securely manage the connection to the user's Bybit account.
-   **Key Components**:
    -   **Navigation Bar**: Same as the dashboard.
    -   **API Credentials Card**:
        -   **Title**: "Bybit API Connection".
        -   **Status Indicator**: A clear "Connected" or "Not Connected" status.
        -   **Instructional Text**: Detailed, security-focused instructions on how to generate an API key on Bybit. It will instruct the user to enable **"Unified Trading"** permissions and explicitly warn them **not** to enable `Assets` permissions (like `Wallet` or `Exchange`). The UI will state that keys with broader permissions than necessary will be rejected for security.
        -   **Form**:
            -   Input field for "API Key".
            -   Input field for "API Secret" (type="password").
        -   **Action Buttons**:
            -   `Save & Validate Keys` button.
            -   `Delete Keys` button (destructive action, requires confirmation).

## 5. Reusable Component Library (`/components/ui/`)

-   **Button**: Variants for `primary`, `secondary`, `destructive`.
-   **Panel/Card**: The main surface for modules.
-   **Input**: Styled text input for forms.
-   **Table**: A styled data table.
-   **Modal**: For confirming critical actions (e.g., executing a trade, deleting API keys).
-   **Navbar**: The main application navigation component.
-   **Chart**: A wrapper for the charting library.
-   **Spinner/Skeleton**: For indicating loading states (e.g., while fetching balance from Bybit).
