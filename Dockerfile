FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libmagic1 gcc libpq-dev unixodbc-dev libgssapi-krb5-2

RUN pip install poetry==1.6.1

WORKDIR /app/vocalvibe

COPY ./app /app/vocalvibe/app
COPY ./pyproject.toml /app/vocalvibe/pyproject.toml
COPY ./migrations /app/migrations
COPY ./alembic.ini /app/alembic.ini
COPY ./Makefile /app/Makefile

RUN poetry config virtualenvs.create false && poetry install --only main --no-ansi --no-root

RUN echo export PATH="$PATH:$HOME/.poetry/bin" >> ~/.bashrc

RUN adduser vocalvibe

USER vocalvibe

COPY ./start.sh /app/vocalvibe/start.sh

CMD ["/bin/bash", "/app/vocalvibe/start.sh"]

