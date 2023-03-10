FROM python
RUN pip install poetry

COPY pyproject.toml poetry.lock /
RUN poetry config virtualenvs.create false
RUN  poetry install --no-dev --no-root
COPY .. /app
WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]