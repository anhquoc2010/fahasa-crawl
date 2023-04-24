FROM python:3.10-slim-buster

WORKDIR /index
COPY ./requirements.txt /index/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /index/requirements.txt
COPY . /index/main

WORKDIR /index/main/main
CMD ["python", "-m", "flask", "run" ,"--host", "0.0.0.0", "--port", "8000"]