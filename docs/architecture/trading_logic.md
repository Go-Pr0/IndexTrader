# Core Trading Logic

This section defines the precise logic for constructing and executing trades for the synthetic BTC.D index.

## Index Composition

A long position on the BTC.D index is synthetically created by allocating a user's capital according to the following fixed ratio:
- **50% Bitcoin (BTC)**
- **50% Altcoin Basket**

## Altcoin Basket Definition

The "Altcoin Basket" is a dynamically selected group of the top 'X' altcoins, designed to mirror the broader altcoin market as closely as possible while respecting exchange-defined trading constraints.

1.  **Asset Universe**: The platform will consider the **top 50 altcoins by market capitalization** that are tradable on Bybit (USDT pairs).
2.  **Dynamic Selection**: The number of altcoins ('X') in the basket for any given trade depends on the user's position size and the minimum trade size for each coin on Bybit.
3.  **Weighting**: The allocation to each of the 'X' altcoins within the basket is weighted relative to its market capitalization compared to the total market cap of the selected 'X' coins.

## Trade Execution & Calculation Logic

To "buy" (go long) BTC Dominance, the system will **long BTC** and **short a basket of altcoins**. To "sell" (go short) BTC Dominance, it does the inverse.

1.  **Total Allocation**:
    *   Capital for BTC (`C_btc`): `S * 0.50`
    *   Capital for Altcoin Basket (`C_alt`): `S * 0.50`

2.  **Fetch Market Data**:
    *   The system reads the pre-calculated **"Asset Universe"** from the `daily_tradable_assets` table in the **General Data DB**.

3.  **Dynamically Build Altcoin Basket**:
    *   The system performs the following sequence to build the basket:
    1. Fetches all tradable USDT perpetual contracts from the daily cached data in the General Data DB.
    2. Fetches the top 100 cryptocurrencies by market cap from the same daily cached data.
    3. Creates an "intersection list" containing only the assets that appear in both lists.
    4. The final **"Asset Universe"** for the trade is the **top 50 assets** from this intersection list, sorted by their market cap ranking. This guarantees every coin considered is both highly ranked and currently tradable.
    5. It then iterates through this final Asset Universe, ordered from highest market cap to lowest.
    *   For each altcoin `i`, it calculates its proportional contribution to the total market cap of the top 50 list.
    *   It then calculates the target allocation for that coin from the altcoin capital: `Target_i = C_alt * (MarketCap_i / TotalMarketCap_top50)`.
    *   **Inclusion Condition**: The altcoin `i` is included in the basket **only if** `Target_i` is greater than or equal to its `minNotionalValue` for its **perpetual futures contract**.
    *   This process continues down the list until the inclusion condition fails, defining the final set of 'X' coins for the basket for that specific trade.

4.  **Final Trade Calculation & Execution**:
    *   The system will re-calculate the weights for only the included 'X' coins to ensure the `C_alt` is fully distributed among them.
    *   It then calculates the exact USDT amount to long for each of the 'X' altcoins and for BTC.
    *   Finally, it executes the trades on the respective perpetual futures contracts using the user's Bybit account API.

## Short Position Execution

When a user requests to "sell" (go short) the BTC.D index with a total position size of `S` (in USDT), the system performs the following mirrored calculation:

1.  **Total Allocation**:
    *   Capital for BTC (`C_btc`): `S * 0.50`
    *   Capital for Altcoin Basket (`C_alt`): `S * 0.50`
2.  **Trade Execution**:
    *   The system executes a **1x leverage market SHORT order** for BTC for a notional value of `C_btc`.
    *   For the dynamically selected altcoin basket, it executes **1x leverage market LONG orders** for a total notional value of `C_alt`.

This creates a position that profits if altcoins outperform Bitcoin, which is the functional equivalent of being short Bitcoin Dominance. The `side` of each trade (`'Long'` or `'Short'`) is recorded in the `trades` table.

5.  **Record Position Snapshot**:
    *   Upon successful execution of all trades, the system immediately writes to the `position_components` table.
    *   For each asset in the position, it creates a new row containing the `position_id`, the `symbol` (e.g., 'BTCUSDT'), and the `expected_quantity` that was just opened. This creates the immutable snapshot for future comparisons.

## Entry Price & P&L Calculation

To ensure accuracy and transparency, the system relies on the Bybit API as the single source of truth for all pricing and performance calculations.

*   **Entry Price**: The entry price for each individual component of a synthetic position is defined as the **actual execution price returned by the Bybit API** in the trade confirmation. This value is non-negotiable and will be permanently stored in the `price` column of our `trades` table. 