FROM python:3.11-alpine

COPY benchmark_api.py .

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python","benchmark_api.py" ]