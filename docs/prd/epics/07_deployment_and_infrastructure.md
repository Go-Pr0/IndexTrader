# Epic 7: Deployment & Infrastructure

## Description

This epic covers all the final steps required to deploy the entire application stack to Render.com. This includes finalizing the `render.yaml` infrastructure-as-code file, setting up production environment variables and secrets, and ensuring the frontend and backend applications are configured for a production environment.

## User Stories

-   As a Platform Operator, I want to deploy the entire application stack—frontend, API, workers, and databases—to Render using a single, version-controlled configuration file.
-   As a Platform Operator, I want to manage all production secrets and environment variables securely through the Render dashboard.
-   As a Developer, I want to ensure the CI/CD pipeline on Render automatically deploys new changes when they are merged into the main branch.

## Technical Requirements

### Infrastructure-as-Code (`render.yaml`)

-   Finalize the `render.yaml` file to define all services:
    -   **Static Site (Next.js Frontend):**
        -   Build command: `npm run build`
        -   Publish directory: `.next`
    -   **Web Service (FastAPI Backend):**
        -   Runtime: Docker
        -   Dockerfile path: `./backend/Dockerfile`
        -   Health check endpoint (e.g., `/api/health`)
    -   **Background Worker (Celery):**
        -   Runtime: Docker
        -   Start command: `celery -A app.workers.celery_app worker -B --loglevel=info` (This runs both the worker and beat in one process for simplicity).
    -   **Redis Instance:**
        -   Standard Render Redis service.
    -   **PostgreSQL Instances (x2):**
        -   One for `User Data DB`.
        -   One for `General Data DB`.
-   **Environment Variable Groups:**
    -   Create groups to share common variables (like database URLs) between the API service and the Celery worker.
-   **Secret Files:**
    -   Configure the `render.yaml` to mount the master encryption key as a secret file at the path specified in the environment variables (e.g., `/etc/secrets/master_key`).

### Configuration

-   **Backend:**
    -   Ensure the Dockerfile is optimized for production (e.g., using a slim base image).
    -   The application must be configured via environment variables set in the Render dashboard.
-   **Frontend:**
    -   Ensure the Next.js application is configured to point to the production backend API URL via `NEXT_PUBLIC_API_URL`.
-   **DNS & Domains:**
    -   Configure custom domains for the frontend and backend services on Render.

## Acceptance Criteria

-   The `render.yaml` file successfully provisions all required infrastructure on Render.
-   The frontend application is successfully built and deployed.
-   The backend Docker container builds successfully and the service starts without errors.
-   The Celery worker connects to Redis and the databases and starts successfully.
-   Environment variables and the master key secret are correctly passed to the running services.
-   The frontend can successfully make API calls to the deployed backend.
-   Automated deployments are triggered upon pushes to the main git branch. 