FROM python:3.10-slim-buster

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY . /api/mysql_api

WORKDIR /api/mysql_api/mysql_api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]