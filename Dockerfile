# syntax=docker/dockerfile:1

# Define Target Python Version
ARG PYTHON_VERSION=3.14

# Begin Build Stage
FROM python:${PYTHON_VERSION}-slim AS build-image

# Prepare system
RUN apt-get update && \
    apt-get install -y gcc python3-dev git ssh curl ca-certificates && \
    apt-get clean

# Download the latest uv installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy the project into the image
COPY . /app

# Configure uv environment
# Use cache mount to improve build times
# Compile to bytecode for faster startup
# Never download python versions during build
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# Set working directory
WORKDIR /app

# Sync project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --no-dev

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-editable --no-dev

# Begin Runtime Stage
FROM python:${PYTHON_VERSION}-slim AS runtime-image

# Install curl and clean up
RUN apt-get update && \
    apt-get install -y curl ca-certificates && \
    apt-get clean

# Create application directory
RUN mkdir -p /app

# Create a non-root user to run the application
RUN groupadd -r app && useradd -r -d /app -g app -N app

# Sey non-root user as owner of the application directory
RUN chown -R app:app /app

# Retrieve packages from the build stage
COPY --from=build-image --chown=app:app /app/.venv /app/.venv
COPY --from=build-image --chown=app:app /app/src /app/src
COPY --from=build-image --chown=app:app /app/alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY pyproject.toml /app/pyproject.toml

# Register the virtual environment
ENV PATH="/app/.venv/bin/:$PATH"

# Switch to non-root user
USER app

# Set working directory
WORKDIR /app

# Add stop signal handler for uvicorn
STOPSIGNAL SIGINT

# Expose application port
EXPOSE 8000

# Start the application with uvicorn
CMD ["poe", "api", "--host", "0.0.0.0", "--port", "8000"]
