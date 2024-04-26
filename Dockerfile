FROM python:3.12.2 as build
RUN pip install pipx
RUN pipx install poetry
ENV PATH="$PATH:/root/.local/bin"

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.in-project true
RUN poetry install --only main

FROM python:3.12.2 as production
LABEL authors="Timofey"

WORKDIR /app
COPY --from=build /app/.venv/ /app/.venv/
COPY ./nta_lab2/ /app/nta_lab2

ENTRYPOINT ["/app/.venv/bin/python", "-m", "nta_lab2"]

