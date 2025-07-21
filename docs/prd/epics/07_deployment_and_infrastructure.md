# Epic 7: Deployment & Infrastructure

## Description

This epic covers all the final steps required to deploy the entire application stack to Railway.app. This includes creating and configuring the `railway.toml` infrastructure-as-code files, setting up production environment variables and secrets, and ensuring the frontend and backend applications are configured for a production environment.

## User Stories

-   As a Platform Operator, I want to deploy the entire application stack—frontend, API, workers, and databases—to Railway using version-controlled configuration files.
-   As a Platform Operator, I want to manage all production secrets and environment variables securely through the Railway dashboard.
-   As a Developer, I want to ensure the CI/CD pipeline on Railway automatically deploys new changes when they are merged into the main branch.

## Technical Requirements

### Infrastructure-as-Code (`railway.toml`)

-   Create `railway.toml` files to define all services:
    -   **Frontend (`frontend/railway.toml`):**
        -   Build command: `npm install && npm run build`
        -   Start command: `npm start`
    -   **Backend (`backend/railway.toml`):**
        -   Defines `api`, `data-poller`, and `trading-engine` services.
        -   Uses a single Dockerfile with different start commands based on `CONTAINER_ROLE`.
    -   **Redis Instance:**
        -   Provisioned through the Railway UI.
    -   **PostgreSQL Instances (x2):**
        -   One for `User Data DB`.
        -   One for `General Data DB`.
        -   Provisioned through the Railway UI.
-   **Environment Variables:**
    -   Configure environment variables for each service in the Railway dashboard.
-   **Secrets Management:**
    -   Store the master encryption key and other secrets securely in Railway's environment variable management system.

### Configuration

-   **Backend:**
    -   Ensure the Dockerfile is optimized for production (e.g., using a slim base image).
    -   The application must be configured via environment variables set in the Railway dashboard.
-   **Frontend:**
    -   Ensure the Next.js application is configured to point to the production backend API URL via `NEXT_PUBLIC_API_URL`.
-   **DNS & Domains:**
    -   Configure custom domains for the frontend and backend services on Railway.

## Acceptance Criteria

-   The `railway.toml` files successfully configure all services on Railway.
-   The frontend application is successfully built and deployed.
-   The backend Docker container builds successfully and all services start without errors.
-   The workers connect to Redis and the databases and start successfully.
-   Environment variables and secrets are correctly passed to the running services.
-   The frontend can successfully make API calls to the deployed backend.
-   Automated deployments are triggered upon pushes to the main git branch. 