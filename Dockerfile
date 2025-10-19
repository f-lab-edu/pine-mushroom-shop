FROM python:3.14

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY . .

WORKDIR /app/src

CMD ["uv", "run", "fastapi", "run"]
