FROM python:3.10

WORKDIR /app/
RUN apt update
RUN apt install -y python3-pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

RUN poetry add flask-login
RUN poetry add python-telegram-bot-pagination
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"
COPY ./app /app
ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]

