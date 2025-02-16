FROM python:3.12-alpine as dev

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

RUN apk add gcc \
            curl \
            musl-dev --no-cache && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apk del curl

COPY ["pyproject.toml", "poetry.lock", "."]

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction \
                   --no-ansi \
                   --no-root \
                   -vvv

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000


FROM dev AS prod

COPY ./library .

RUN python -m pip install gunicorn

CMD gunicorn --bind 0.0.0.0:8000 library.wsgi


FROM dev AS test

CMD python manage.py migrate && echo 'Run tests' && python manage.py test apps.accounts apps.books.tests
