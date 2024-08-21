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

# Dependencies installation
COPY ./requirements.txt /expmotor/requirements.txt
COPY ./requirements_dev.txt /expmotor/requirements_dev.txt
RUN uv pip install --system -r /expmotor/requirements_dev.txt

# Copy project
COPY . /expmotor

# Alter entrypoint script
RUN sed -i 's/\r$//g' /expmotor/compose/production/entrypoint.sh
RUN chmod +x /expmotor/compose/production/entrypoint.sh

# Alter startup script
RUN sed -i 's/\r$//g' /expmotor/compose/production/startup_web.sh
RUN chmod +x /expmotor/compose/production/startup_web.sh

# Specify network port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/expmotor/compose/production/entrypoint.sh"]
