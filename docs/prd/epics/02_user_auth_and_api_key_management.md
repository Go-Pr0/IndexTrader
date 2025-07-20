# Epic 2: User Authentication & API Key Management

## Description

This epic focuses on creating a secure and seamless authentication experience for users and providing a robust mechanism for managing their Bybit API keys. This involves both frontend and backend work, implementing user sign-up/sign-in via NextAuth.js and developing the backend services for securely storing and validating user-provided API keys.

## User Stories

-   As a User, I want to sign up and log in to the platform using my Google account so that I can access the service without creating a new password.
-   As a User, I want a dedicated settings page where I can securely add, validate, and delete my Bybit API keys so that I can connect my exchange account to the platform.
-   As a Platform Operator, I want to ensure that user API keys are encrypted at rest using a master key stored securely outside of environment variables so that we can protect sensitive user credentials.
-   As a Developer, I want to programmatically validate that user-provided Bybit keys have only the necessary "Unified Trading" permissions and reject keys with excessive permissions to enhance security.

## Technical Requirements

### Frontend (Next.js)

-   **Authentication (`lib/auth.ts`, `app/auth/...`):**
    -   Integrate NextAuth.js.
    -   Configure the Google OAuth provider.
    -   Protect the `/dashboard` and `/settings` routes, requiring authentication.
    -   Create login/logout UI flows.
-   **Settings Page (`app/settings/page.tsx`):**
    -   Build the UI as per the `frontend.md` specification.
    -   Include a form for submitting API key and secret.
    -   Display clear instructions for creating the key on Bybit with the correct permissions (**Unified Trading** only).
    -   Provide clear feedback on whether the key is "Connected" or "Not Connected".
    -   Implement "Save" and "Delete" functionality, with confirmation modals for destructive actions.
-   **API Integration (`lib/api.ts`):**
    -   Create functions to communicate with the backend `/api/credentials` endpoint.

### Backend (Python/FastAPI)

-   **API Endpoints (`api/endpoints/credentials.py`):**
    -   `POST /api/credentials`: Receives API key/secret, validates them with Bybit, encrypts them, and saves to the `bybit_credentials` table.
    -   `GET /api/credentials/status`: Checks if a key is stored for the authenticated user and returns its status.
    -   `DELETE /api/credentials`: Deletes the credentials for the authenticated user.
-   **Security (`services/security.py`):**
    -   Implement AES-256 encryption/decryption logic.
    -   The service must read the master key from the path specified by the `RENDER_MASTER_KEY_PATH` environment variable. The plaintext key should only be held in memory.
-   **Bybit Service (`services/bybit_api.py`):**
    -   Create a service to interact with the Bybit API via the `pybit` library.
    -   Implement a function to validate API key permissions. It must check that the key has **only** the **"Unified Trading"** permission enabled and reject any key that has additional permissions like `Assets` or `Withdrawal`.
-   **Database Schema (`db/models.py`):**
    -   Define the `users` and `bybit_credentials` tables using SQLAlchemy ORM.
    -   The `users` table will be managed by NextAuth.js, but the model is needed for relationships.
    -   `bybit_credentials` table must have `user_id` (PK, FK), `encrypted_api_key`, and `encrypted_api_secret` (both `BYTEA`).

## Acceptance Criteria

-   Users can sign up and log in using Google.
-   Authenticated users can access the `/settings` page.
-   Users can submit their Bybit API key and secret. The system correctly validates the key's permissions with Bybit.
-   Valid keys are encrypted with AES-256 and stored in the `bybit_credentials` table.
-   Invalid keys (wrong permissions, incorrect credentials) are rejected with a clear error message to the user.
-   The settings page correctly reflects the connection status.
-   Users can delete their saved keys.
-   The master encryption key is successfully read from a secret file, not an environment variable. 