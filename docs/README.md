## Documentation utilisateur

### Prérequis

- Python 3.10    https://www.python.org/downloads/
- git            https://git-scm.com/downloads
- Docker         https://docs.docker.com/get-docker/
- Kubernetes     https://kubernetes.io/fr/docs/tasks/tools/install-kubectl/

### Installation

Voir le fichier [README.md](../README.md)

### Utilisation de l'application en local :

1 - Une fois l'application lancée, les routes de l'API et la documentation sont disponibles à l'adresse suivante :

http://localhost:81/docs

Vous devriez voir la documentation de l'API.
![img.png](imgs/01.png)

Note : le port 81 est configuré uniquement pour l'environnement de développement. Une fois l'application déployée en
production, le port 443 sera utilisé.

2 - Pour tester l'API, il faut d'abord créer un token en utilisant la route :

http://localhost:82/api/v1/create-token/{token_id}/{mdp}

Vous devez remplacer {token_id} et {token_id} par les valeurs de votre choix.


Cliquer sur l'icone cadnas pour ouvrir la fenêtre d'authentification.

Puis saisir le token à utiliser est : admin

![img.png](imgs/02.png)

Cliquer sur Authorize et close pour valider.

Ensuite cliquer sur Try it out.

entrer dans le champs token_id "57" et le mot de passe "test"
![img.png](imgs/03.png)

ce qui doit donner un token:

``eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdCIsImV4cCI6MTY4OTc3NDQ3OH0.x0FNITaFEyxqiRzJYaWAqC5Iy12MgWTr2EsG1NoPuFs``

Puis sur execute pour exécuter la requête.

Si la requête est exécutée avec succès, vous devriez voir le message suivant :
![img.png](imgs/04.png)

3 - Pour requeter les APIs Product et Customers :

Déconnectez vous avec le token admin et reconnectez vous avec le token generer avec le mot de passe test dont je vous recopie le token:

``eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdCIsImV4cCI6MTY4OTc3NDQ3OH0.x0FNITaFEyxqiRzJYaWAqC5Iy12MgWTr2EsG1NoPuFs``

remplacer le token admin par le token ci dessus dans l'onglet cadenas

![img.png](imgs/05.png)

Vous pouvez maintenant tester les APIs Products et Customers

Customers

![img.png](imgs/06.png)

![img.png](imgs/07.png)

Products

![img.png](imgs/08.png)

![img.png](imgs/09.png)