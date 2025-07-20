# Architecture Overview

This document provides the technical architecture for the Non-Custodial Index Trading Platform MVP. It is based on the latest Product Requirements Document and is designed to create a secure, reliable, and simple system for remotely controlling a user's Bybit account to trade synthetic indices.

The architecture's primary focus is the secure handling of user API keys and the robust, transparent execution of trades on the user's behalf.

## High-Level Architecture

The system is designed as a modern web application with a decoupled frontend and a modular backend. It will be deployed on the Render.com platform. The architecture is simplified to reflect its non-custodial nature, focusing on three core external interactions: the user, the Bybit API, and the CoinDesk API for market data.

### System Components Diagram (C4 Model - Level 2)

```
+---------------------------------+
|            End User             |
+---------------------------------+
          |
          v
+---------------------------------+
|     Frontend Web Application    |
|   (Next.js with NextAuth.js)    |
+---------------------------------+
          | (API Calls)
          v
+---------------------------------+
|      API Service (FastAPI)      |
|    (Enqueues Tasks, Serves UI)  |
+---------------------------------+
          | (Enqueues Tasks)
          v
+---------------------------------+
|      Message Broker (Redis)     |
+---------------------------------+
     ^    |
(Status) | (Pulls Tasks)
     |    v
+---------------------------------+
|       Celery Workers            |
|  (Execute All Business Logic)   |
+---------------------------------+
     |      |      |
     v      v      v (Bybit, CoinGecko)
+----------------+  +----------------+
| User Data DB   |  | General Data DB|
| (PostgreSQL)   |  | (PostgreSQL)   |
+----------------+  +----------------+

```

### Component Responsibilities

-   **Frontend Web Application**: A client-side Next.js application that handles all user-facing elements. **Authentication is managed directly by NextAuth.js**, which handles sign-in flows and session management.
-   **API Service (FastAPI)**: A lightweight **Render Web Service** that serves as the primary entry point. Its main responsibilities are to handle user authentication, validate incoming requests, and **enqueue tasks** for the Celery workers. It does not perform any heavy, long-running business logic itself.
-   **Message Broker (Redis)**: Acts as the central nervous system for the backend, managing the queues of tasks to be executed.
-   **Celery Workers**: One or more **Render Background Workers** that are the workhorses of the system. They pull tasks from the Redis queue and execute all the core business logic: interacting with the Bybit and CoinGecko APIs, performing trade calculations, and updating the databases.
-   **Celery Beat**: A scheduler process (can run as part of a worker) that periodically enqueues recurring tasks, such as daily data polling and position reconciliation.
-   **PostgreSQL Databases (Render)**: The system uses two separate PostgreSQL databases for security and data isolation:
    -   **User Data DB**: The primary data store for all sensitive and user-specific information, including user accounts, encrypted API keys, and trade/position history.
    -   **General Data DB**: Stores non-sensitive, general market data, specifically the daily list of tradable assets and their properties.
-   **External Services**:
    -   **Bybit**: The user's crypto exchange, where all funds are held and all trades are executed.
    -   **CoinGecko**: The source of market capitalization data for asset ranking.
    -   **NextAuth.js Supported Providers (e.g., Google)**: For handling the OAuth 2.0 sign-in flows.

## Technology Stack

| Category             | Technology         | Justification                                                                 |
| -------------------- | ------------------ | ----------------------------------------------------------------------------- |
| **Frontend**         | **Next.js (React)**| For building a fast and modern user interface.                                |
| **Authentication**   | **NextAuth.js**    | A full-featured authentication library for Next.js that simplifies handling sessions, social logins, and JWTs. For the MVP, this will be configured to use the **Google OAuth provider**. |
| **Backend**          | **Python 3.11+**   | Strong ecosystem for interacting with crypto exchange APIs and data analysis. |
| **Backend Framework**| **FastAPI**        | High performance and excellent for building a robust API service.               |
| **API Clients**      | **Pybit & PyCoingecko** | To ensure reliable and maintainable interaction with external services, the backend will use these established client libraries for all Bybit and CoinGecko API communications. |
| **Asynchronous Task Queue** | **Celery & Redis** | Celery is a robust, production-ready task queue. Using it with Redis allows for scalable, asynchronous execution of all long-running tasks (like trade execution), ensuring the API remains fast and responsive. |
| **Database**         | **PostgreSQL**     | A reliable relational database for storing user and trade data.               |
| **ORM**              | **SQLAlchemy 2.0** | Provides a robust and secure layer for database interaction.                    |
| **Background Jobs**  | **Celery**         | A production-ready task queue for running the data poller.                    |
| **Containerization** | **Docker**         | Standardizes the development and deployment environment.                      |
| **Infrastructure**   | **Render.com**     | A unified PaaS for deploying the entire application stack.                    | 