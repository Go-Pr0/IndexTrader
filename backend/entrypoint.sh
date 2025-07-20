#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Default to running the API server if CONTAINER_ROLE is not set.
if [ -z "$CONTAINER_ROLE" ]; then
  echo "CONTAINER_ROLE not set, defaulting to api"
  CONTAINER_ROLE=api
fi

echo "Container role: $CONTAINER_ROLE"

# Execute the appropriate command based on the CONTAINER_ROLE.
if [ "$CONTAINER_ROLE" = "api" ]; then
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
elif [ "$CONTAINER_ROLE" = "data-poller" ]; then
  exec celery -A app.workers.tasks worker -l info -Q data-tasks -n data-poller@%h
elif [ "$CONTAINER_ROLE" = "trading-engine" ]; then
  exec celery -A app.workers.tasks worker -l info -Q trading-tasks -n trading-engine@%h
else
  echo "Error: Unknown CONTAINER_ROLE: $CONTAINER_ROLE"
  exit 1
fi 