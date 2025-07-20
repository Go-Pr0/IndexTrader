# Database Architecture

## Database Schema

The schema is now split into two separate databases to isolate user data from general market data.

### User Data DB Schema

#### `users`
- `id` (PK, from NextAuth.js), `name`, `email` (UNIQUE), `image`, `emailVerified` (TIMESTAMP), `subscription_tier` (VARCHAR, default: 'free')
- *This table is managed by NextAuth.js. The `subscription_tier` column is included to facilitate future implementation of premium plans without requiring a complex data migration. For the MVP, all users will have the 'free' tier.*

#### `bybit_credentials`
- `user_id` (PK, FK to users.id), `encrypted_api_key` (BYTEA), `encrypted_api_secret` (BYTEA), `updated_at`
- *Stores the encrypted keys for each user. One-to-one relationship with users.*

#### `synthetic_positions`
- `id`, `user_id` (FK), `index_name`, `usdt_size`, `status` (e.g., 'PENDING', 'EXECUTING', 'ACTIVE', 'FAILED'), `is_altered`, `unrealized_pnl`, `created_at`, `updated_at`
- *A record of the high-level positions the user has opened.*

#### `position_components`
- `id`, `position_id` (FK), `symbol` (e.g., 'BTCUSDT'), `expected_quantity` (NUMERIC)
- *A snapshot of the target composition of a synthetic position at the moment of its creation. This table is the source of truth for what the position *should* be.*

#### `trades`
- `id`, `position_id` (FK), `bybit_order_id`, `symbol` (e.g., 'BTCUSDT'), `side` ('Long' or 'Short'), `price`, `quantity`, `timestamp`
- *An audit log of all the individual trades executed on Bybit to create or close a synthetic position.*

### General Data DB Schema

#### `daily_tradable_assets`
- `id`, `symbol` (e.g., 'BTCUSDT'), `market_cap_rank` (INTEGER), `min_notional_value` (NUMERIC), `fetch_date` (DATE)
- *A daily snapshot of the assets that make up the tradable universe, populated by the Data Poller worker.*

## Database Migrations

All changes to the PostgreSQL database schemas (for both the User Data DB and the General Data DB) will be managed using **Alembic**. Every modification to a table must be accompanied by a new, version-controlled Alembic migration script. This practice ensures that database schema changes are repeatable, testable, and can be applied safely and consistently across all environments. 