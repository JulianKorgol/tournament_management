FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY /backend/requirements.txt /app/requirements.txt

COPY /backend/docker_script.sh /app/docker_script.sh

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
	&& pip install -r /app/requirements.txt