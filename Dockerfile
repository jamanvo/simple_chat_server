FROM python:3.12
WORKDIR /app
RUN apt update && apt install -y vim libsasl2-dev python3-dev libssl-dev

RUN pip install poetry pip setuptools wheel --upgrade
COPY pyproject.toml /app
COPY poetry.lock /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root
