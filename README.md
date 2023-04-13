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

http://localhost:8000/docs

## Docker

### Build (se mettre dans le dossier racine du projet) :

```sh
docker build -t webshop_api -f ./deployment/Dockerfile .
```

### Lance le container :

```sh
docker run -p 8000:8000 webshop_api
```