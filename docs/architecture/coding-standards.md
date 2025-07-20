# Coding Standards

This document defines the coding standards and conventions to be followed for the project. Adhering to these standards is crucial for maintaining code quality, readability, and consistency across the codebase.

## General Principles

1.  **Clarity and Readability**: Write code that is easy to understand. Prioritize clarity over cleverness. Use meaningful variable and function names.
2.  **DRY (Don't Repeat Yourself)**: Avoid duplicating code. Abstract and reuse components, functions, and services where appropriate.
3.  **YAGNI (You Ain't Gonna Need It)**: Do not add functionality or complexity that is not required by the current user stories.
4.  **Single Responsibility Principle (SRP)**: Each module, class, and function should have a single, well-defined responsibility.

---

## Python (Backend)

-   **Formatting**: All Python code **must** be formatted using `black`. This is non-negotiable and will be enforced by CI checks.
-   **Linting**: Use `ruff` for linting to catch common errors and style issues.
-   **Type Hinting**: All function signatures and variable declarations **must** include type hints. This is critical for maintaining a large, modular codebase.
-   **Docstrings**: Use Google-style docstrings for all public modules, classes, and functions to explain their purpose, arguments, and return values.
-   **Dependencies**: All dependencies must be explicitly listed in `requirements.txt`. Use a tool like `pip-tools` to manage and pin versions for reproducible builds.
-   **Testing**: While not implemented in the MVP, the structure should allow for future unit and integration tests using `pytest`. Test files should be co-located with the code they are testing in a `tests/` subdirectory.
-   **Imports**: Imports should be organized into three groups, separated by a blank line:
    1.  Standard library imports (e.g., `os`, `sys`).
    2.  Third-party library imports (e.g., `fastapi`, `sqlalchemy`).
    3.  Local application imports (e.g., `from app.core import config`).

## TypeScript/React (Frontend)

-   **Formatting**: All TypeScript/JavaScript code **must** be formatted using `prettier`. This will be enforced by CI checks.
-   **Linting**: Use `eslint` to enforce code quality and catch common errors. The configuration should extend recommended rulesets for React and TypeScript.
-   **Component Structure**:
    -   Components should be organized by feature or page in the `src/components` directory.
    -   Reusable, generic UI components (e.g., `Button`, `Card`) should reside in `src/components/ui`.
    -   Favor functional components with Hooks over class components.
-   **State Management**: For the MVP, local component state (`useState`, `useReducer`) and React Context are sufficient. Avoid introducing a global state management library (like Redux or Zustand) until a clear need arises.
-   **Styling**: Use Tailwind CSS for all styling. Avoid writing custom CSS files or using CSS-in-JS libraries to maintain consistency.
-   **Naming Conventions**:
    -   Component files and functions: `PascalCase` (e.g., `PositionsPanel.tsx`).
    -   Variables and functions: `camelCase`.
    -   Interfaces and type aliases: `PascalCase` (e.g., `interface UserProfile`).

## Git & Version Control

-   **Branching Strategy**: Use a simplified GitFlow model.
    -   `main`: The production branch. All commits to `main` should be via Pull Request and trigger a production deployment.
    -   `feature/<name>`: All new work must be done on a feature branch. Branch names should be descriptive (e.g., `feature/add-pnl-column`).
-   **Commit Messages**: Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. This helps in automating changelogs and makes the commit history more readable.
    -   Example: `feat(api): add endpoint for closing positions`
    -   Example: `fix(frontend): correct P&L color for negative values`
    -   Example: `docs(arch): update source tree diagram`
-   **Pull Requests (PRs)**:
    -   All PRs into `main` must be reviewed by at least one other team member.
    -   PRs should be small and focused on a single feature or fix.
    -   The PR description should clearly explain the "what" and "why" of the change. Link to the relevant user story or issue. 