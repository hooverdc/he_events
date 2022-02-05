FROM python:3.10-alpine

WORKDIR /usr/src/app

COPY requests.txt .

RUN pip install -r requests.txt

COPY src .

CMD ["python", "main.py"]
