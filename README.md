# MSPR_Bloc_4_API_webshop

Ce repository contient le code source de l'API Webshop.

## Constitution du groupe :

- Adel Ould Ouelhadj
- Boudjemaa AKHAM
- Guillaume GAY
- Jean-Daniel SPADAZZI
- Sébastien GLORIES

### Résumé de l'API Revendeur :

L'API Webshop gere les demande du site internet. authentifier par un token, elle permet d'acceder aux partie gestion des clients (customers) et a la partie produit et ces details (products). 

### Pratiques de développement (gitflow) :

- La branche main est la branche de production.
- La branche preprod est la branche de pré-production.
- Les branches de développement sont les branches nomées par les noms des développeurs. Chaque développeur a sa branche
  de développement pour développer les fonctionnalités qui lui sont assignées.
- Les branches nomées fix sont les branches de correction de bugs. Elles sont créées à partir de la branche de
  développement du développeur qui a corrigé le bug.
- Les branches nomées test sont les branches de test. Elles sont créées à partir de la branche de développement du
  développeur qui a développé la fonctionnalité à tester.

# utilisation de l'application

1- Cloner le repository : (Demander l'accès au repository à l'un des membres du groupe)

```bash
git clone https://github.com/BoudjemaaAKHAM/MSPR_Bloc_4_API_Webshop.git
```
2- Créer un environnement virtuel.

3- Installer localement l'application :

```bash
RUN pip install -e .
```

4- Lancer l'application :

```bash
python -m webshopapi.main
``` 

5- les routes de l'API et la documentation sont disponibles à l'adresse suivante :
http://localhost:81/docs

6- Pour lancer les tests unitaires :

```bash
py -m pytest ./unittests -v --junit-xml ./unittests/report.xml
```

<!-- 7- lancer les tests unitaires avec coverage :

```bash
py -m pytest ./unittests -v --junit-xml ./unittests/report.xml --cov=. --cov-report=html
``` -->

### Utilisation de l'application avec Docker :

1- Créer l'image Docker :

```bash
docker build -t webshop_api -f ./deployment/Dockerfile .
```

2- Lancer l'application :

```bash
docker run -p 445:445 webshop_api
```

3- les routes de l'API et la documentation sont disponibles à l'adresse suivante :
https://localhost:445/docs

### Push sur DockerHub :

1- Se connecter à DockerHub :

```bash
docker login -username=boudjemaa
```

Saisir le token qui est dans le fichier .dockerhub_token

2- Tagger l'image :

```bash
docker tag webshop_api boudjemaa/webshop_api:latest
```

3- Pusher l'image :

```bash
docker push boudjemaa/webshop_api:latest
```

### Run container on production server

```bash
docker pull boudjemaa/webshop_api:latest
```

```bash
docker run -d --name webshopapi --restart=always -p 442:442 boudjemaa/webshop_api
```

## Utilisation de l'application avec Kubernetes :

### Prérequis

- minikube
- kubectl

### Lancement du cluster

```sh
minikube start
```

### Déploiement de l'application

```sh
kubectl apply -f deployment/k8s-deployment.yaml
```

### Accès à l'application

```sh
minikube service webshop-api
```

ou via lens (https://k8slens.dev/) application desktop pour kubernetes