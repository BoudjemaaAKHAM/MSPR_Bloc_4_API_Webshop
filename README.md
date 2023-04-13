## MSPR_Bloc_4

Repo git pour la mise en situation professionnelle reconstituée du bloc de compétences 4.

## Constitution du groupe :

- Adel Ould Ouelhadj
- Boudjemaa AKHAM
- Guillaume GAY
- Jean-Daniel SPADAZZI
- Sébastien GLORIES

# utilisation de l'application

## Prérequis

```sh
pip install -r requirements.txt
```

## Lancer l'application

```sh
python -m api.main
```

## Les APIs sont accessibles à l'adresse suivante :

http://localhost:81/docs

## Docker

### Build (se mettre dans le dossier racine du projet) :

```sh
docker build -t webshop_api -f ./deployment/Dockerfile .
```

### Lance le container :

```sh
docker run -p 81:81 webshop_api
```

# Kubernetes

## Prérequis

- minikube
- kubectl

## Lancement du cluster

```sh
minikube start
```

## Déploiement de l'application

```sh
kubectl apply -f deployment/k8s-deployment.yaml
```

## Accès à l'application

```sh
minikube service webshop-api
```

ou via lens (https://k8slens.dev/) application desktop pour kubernetes

