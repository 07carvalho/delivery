FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.1.6
RUN apt update && \
    apt install -y gdal-bin
RUN pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
RUN pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-dev
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt
COPY . .
COPY server/.env.dev ./code/server/.env
COPY ./entrypoint.sh ./entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["sh", "/code/entrypoint.sh"]
