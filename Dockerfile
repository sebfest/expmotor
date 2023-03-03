# Base Image
FROM python:3.9

#Maintainer
LABEL maintainer="Sebastian Fest <sebastian.fest@nhh.no>"

# Set working directory
WORKDIR /app

# Install wait-for-it package
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y wait-for-it

# Python Interpreter Flags
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Django flags
ENV DJANGO_SETTINGS_MODULE=settings.local

# Dependencies installation
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements_dev.txt /app/requirements_dev.txt
RUN pip install --upgrade --quiet pip && pip install --no-cache-dir --quiet -r /app/requirements_dev.txt

# Copy project
COPY . /app/

# Alter entrypoint script
COPY ./compose/local/entrypoint.sh /app/compose/local/entrypoint.sh
RUN chmod +x /app/compose/local/entrypoint.sh

##Copy startup script
COPY ./compose/local/entrypoint_web.sh /app/compose/local/entrypoint_web.sh
RUN chmod +x /app/compose/local/entrypoint_web.sh

# Specify network port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT [ "/app/compose/local/entrypoint.sh" ]


