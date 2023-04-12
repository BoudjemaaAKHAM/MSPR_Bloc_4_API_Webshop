# FROM python:3.10-alpine
# FROM python:3.10

# Ouvrir le port 1883 pour les connexions MQTT
# EXPOSE 1883

# WORKDIR /app

# COPY ./app_a/app_a_1/* /app
# COPY ../../mqtt_protocol /app/mqtt_protocol

# Inutile pour éxécuter l'app
#RUN apk add --no-cache build-base

# Décommenter/Commenter si besoin d'installer des dépendances
# COPY ./app_a/app_a_1/requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# WORKDIR /app/mqtt_protocol
# RUN pip install -e .

# WORKDIR /app
# RUN pip install -e .

# CMD ["python", "app_a.py"]

#-----------------------------------
# WORKDIR /api

# COPY requirements.txt .
# RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# EXPOSE 8081
# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8081"]

#-----------------------------------

# WORKDIR /api

# # COPY ./api /api 

# # COPY requirements.txt .
# COPY ./requirements.txt requirements.txt
# RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# EXPOSE 8081
# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8081"]

#-----------------------------------
FROM python:3.10-alpine
# WORKDIR /usr/src/app
WORKDIR /api/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9001

# CMD [ "python", "./app.py" ]
CMD ["uvicorn", "src.app:app", "--reload", "--host", "0.0.0.0", "--port", "9001"] 
# parce que il le demare sur linux on laisse  a 0.0.0.0

#"192.168.65.4"

#-----------------------------------

# FROM python:3.10

# WORKDIR /backend

# COPY requirements.txt .
# RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# EXPOSE 9001
# CMD ["uvicorn", "src.app:app", "--reload", "--host", "0.0.0.0", "--port", "9001"]