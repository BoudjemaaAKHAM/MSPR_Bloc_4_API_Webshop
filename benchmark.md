## Documentation de l'API Customers

L'API Customers permet de gérer des clients.

### Endpoint :

https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers

### Méthodes HTTP :

L'API Customers supporte les méthodes HTTP suivantes :

GET : Récupère la liste des clients ou un client spécifique.
POST : Crée un nouveau client.
PUT : Met à jour un client existant.
DELETE : Supprime un client existant.
Paramètres de requête

#### L'API Customers supporte les paramètres de requête suivants :

id : Identifiant du client à récupérer.
Exemples d'utilisation
Récupérer la liste des clients

```bash
GET /api/v1/customers
```

Retourne la liste des clients au format JSON :

Récupérer un client spécifique

```bash
GET /api/v1/customers?id=1
```

Retourne le client ayant l'identifiant 1
