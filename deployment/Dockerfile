FROM python:3.10-alpine

WORKDIR /app

RUN pip install --upgrade pip

COPY data data
COPY database database
COPY webshopapi webshopapi
COPY utilities utilities
COPY ssl ssl
COPY requirements.txt requirements.txt
COPY setup.py setup.py

RUN pip install -e .


EXPOSE 81
EXPOSE 443

CMD ["uvicorn", "webshopapi.main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/ssl/key.pem", "--ssl-certfile", "/app/ssl/cert.pem"]