# 1. Builder stage: Install dependencies
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 2. Final stage: Create the production image
FROM python:3.11-slim as final

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set environment variables
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

# Copy the application code
COPY ./app /app/app

# Copy the entrypoint script
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port and run the application
ENTRYPOINT ["/app/entrypoint.sh"] 