# Epic 3: Core Data & Trading Logic

## Description

This epic establishes the core intellectual property of the platform: the data polling and trade calculation engine. It involves creating backend services to fetch and store market data from CoinGecko, defining the database schemas for all trading-related entities, and implementing the precise, non-trivial logic for calculating the composition of the BTC.D index based on dynamic market conditions.

## User Stories

-   As a Platform Operator, I want to periodically poll market data (e.g., top assets by market cap) from CoinGecko and store it so that the platform has a reliable, internal source of data for trade calculations.
-   As a Developer, I want to implement the BTC.D index composition logic precisely as specified so that trades accurately reflect the intended 50/50 BTC vs. Altcoin Basket strategy.
-   As a Developer, I want to create a dynamic altcoin basket selection algorithm that respects Bybit's minimum notional value for each asset so that all calculated trades are executable.

## Technical Requirements

### Backend (Python/FastAPI)

-   **Data Polling Worker (`workers/data_poller.py`):**
    -   Create a Celery task that runs on a daily schedule (via Celery Beat).
    -   This task will:
        1.  Fetch the top 100 cryptocurrencies by market cap from CoinGecko using the `pycoingecko` library.
        2.  Fetch the list of all tradable USDT perpetual contracts from Bybit.
        3.  Create an "intersection list" of assets that are in both lists.
        4.  Store the top 50 assets from this intersection list, along with their market cap rank and minimum notional value (from Bybit), into the `daily_tradable_assets` table.
        5.  This task populates the **General Data DB**.
-   **Trading Logic Service (`services/trading_logic.py`):**
    -   This is a pure calculation service; it does not execute trades.
    -   **Function `calculate_trade_composition(usdt_size, direction)`:**
        1.  Takes the total position size and direction ('Long' or 'Short') as input.
        2.  Reads the latest asset universe from the `daily_tradable_assets` table.
        3.  Implements the dynamic altcoin basket creation logic as defined in `architecture.md`:
            -   Allocate 50% of capital to BTC and 50% to the altcoin basket.
            -   Iterate through the top 50 altcoins, including an asset in the basket only if its target allocation is `>=` its `min_notional_value`.
            -   Re-calculate weights for the final included altcoins to ensure 100% of the altcoin capital is used.
        4.  Returns a structured object detailing the exact list of symbols and the USDT amount to be traded for each (e.g., `{'BTCUSDT': 500, 'ETHUSDT': -120, 'SOLUSDT': -80, ...}`).
-   **Database Schema (`db/models.py`):**
    -   **User Data DB:**
        -   `synthetic_positions`: `id`, `user_id`, `index_name`, `usdt_size`, `status`, `is_altered`, `unrealized_pnl`.
        -   `position_components`: `id`, `position_id`, `symbol`, `expected_quantity`.
        -   `trades`: `id`, `position_id`, `bybit_order_id`, `symbol`, `side`, `price`, `quantity`, `timestamp`.
    -   **General Data DB:**
        -   `daily_tradable_assets`: `id`, `symbol`, `market_cap_rank`, `min_notional_value`, `fetch_date`.
-   **Dependencies (`requirements.txt`):**
    -   Add `pycoingecko`, `pybit`.

## Acceptance Criteria

-   The data poller Celery task successfully fetches data from CoinGecko and Bybit and populates the `daily_tradable_assets` table.
-   The `calculate_trade_composition` function correctly implements the dynamic basket logic.
-   Given a position size, the calculation function returns the correct trade composition, respecting the minimum notional value constraints.
-   All required database tables are created via Alembic migrations in their respective databases.
-   The logic correctly distinguishes between a long BTC.D (long BTC, short Alts) and a short BTC.D (short BTC, long Alts) position. 