FROM python:3.13

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY quote-bot ./quote-bot

RUN touch README.md

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "-m", "quote-bot.main"]
