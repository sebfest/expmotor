# Base Image
FROM python:3.11
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

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
RUN apt update -qy && apt install -qy wait-for-it

# Dependencies installation
COPY ./requirements/requirements.txt /expmotor/requirements/requirements.txt
COPY ./requirements/requirements_dev.txt /expmotor/requirements/requirements_dev.txt
RUN uv pip install --system -r /expmotor/requirements/requirements_dev.txt

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
