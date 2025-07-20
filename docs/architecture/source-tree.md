# Source Tree

This document outlines the directory structure and the purpose of key files for both the frontend and backend of the application.

## High-Level Project Structure

```
/
├── backend/            # Python FastAPI Backend
├── frontend/           # Next.js Frontend
├── docs/               # Project documentation (PRD, Architecture, Stories)
├── .github/            # CI/CD workflows and issue templates
├── render.yaml         # Infrastructure-as-Code for Render deployment
└── ...                 # Other root-level configuration files
```

---

## Backend Source Tree (`/backend`)

The backend is a modular monolith designed for a clean separation of concerns.

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/      # API endpoint routers
│   │       ├── __init__.py
│   │       ├── credentials.py
│   │       └── positions.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py       # Pydantic settings management
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py       # SQLAlchemy ORM models
│   │   └── session.py      # Database session and engine setup
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bybit_api.py    # Service for all Bybit API interactions
│   │   ├── security.py     # AES encryption/decryption for API keys
│   │   └── trading_logic.py# Core calculation for index composition
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py   # Celery application definition
│   │   ├── data_poller.py  # Worker for fetching market data
│   │   ├── position_reconciler.py # Worker for P&L and deviation checks
│   │   └── trade_executor.py # Worker for executing trades
│   └── main.py             # FastAPI application entry point
│
├── alembic/                # Alembic migration scripts
├── alembic.ini             # Alembic configuration
├── Dockerfile              # Docker container definition
└── requirements.txt        # Python package dependencies
```

---

## Frontend Source Tree (`/frontend`)

The frontend is a standard Next.js application with a focus on component-based architecture.

```
frontend/
├── src/
│   ├── app/
│   │   ├── (api)/          # API route handlers (e.g., for NextAuth)
│   │   ├── (auth)/         # Authentication-related pages (callback, login)
│   │   ├── dashboard/
│   │   │   └── page.tsx    # The main user dashboard
│   │   ├── settings/
│   │   │   └── page.tsx    # Page for managing API keys
│   │   ├── layout.tsx      # Root application layout
│   │   ├── page.tsx        # Public landing page
│   │   └── globals.css     # Global styles
│   │
│   ├── components/
│   │   ├── dashboard/      # Components specific to the dashboard page
│   │   ├── layout/         # Layout components (Navbar, Footer)
│   │   ├── settings/       # Components specific to the settings page
│   │   └── ui/             # Reusable, generic UI components (Button, Card, Modal)
│   │
│   └── lib/
│       ├── api.ts          # Client-side functions for calling the backend API
│       └── auth.ts         # NextAuth.js configuration and options
│
├── public/                 # Static assets (images, fonts)
├── next.config.ts          # Next.js configuration
├── tailwind.config.ts      # Tailwind CSS configuration
└── tsconfig.json           # TypeScript configuration
``` 