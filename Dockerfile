# Base Image
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /bin/uv

#Maintainer
LABEL maintainer="Sebastian Fest <sebastian.fest@nhh.no>"

# Set working directory
WORKDIR /expmotor

# Python Interpreter Flags
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Django flags
ENV DJANGO_SETTINGS_MODULE=settings.local

# Install wait-for-it package
RUN apt-get update \
    && apt-get install -y --no-install-recommends wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Dependencies installation
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked
ENV PATH="/expmotor/.venv/bin:$PATH"

# Copy project
COPY . /expmotor

# Alter entrypoint script
RUN sed -i 's/\r$//g' /expmotor/compose/local/entrypoint.sh
RUN chmod +x /expmotor/compose/local/entrypoint.sh

# Alter startup script
RUN sed -i 's/\r$//g' /expmotor/compose/local/startup_web.sh
RUN chmod +x /expmotor/compose/local/startup_web.sh

# Specify network port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/expmotor/compose/local/entrypoint.sh"]
