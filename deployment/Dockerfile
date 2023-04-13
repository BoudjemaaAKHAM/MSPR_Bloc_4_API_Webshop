FROM python:3.10-alpine

WORKDIR /app

COPY setup.py setup.py

RUN pip install -e .

# copy only the api folder to the container
COPY webshopapi webshopapi

EXPOSE 81

CMD ["uvicorn", "webshopapi.main:app", "--host", "0.0.0.0", "--port", "81"]