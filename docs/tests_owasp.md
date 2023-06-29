## Pour les test OWASP nous allons verrifier certains de ces test sur notre application API.

1 - Dans un premier temps nous allons commencer avec le test OWASP N°5
    ce test concerne le manque d'acces et de controle

pour cela nous allons tester a partir du DOM pour voir si on peut modifier des éléments:

nous allons tester a partir de la creation d'un User sur l'API de Webshopapi. 
    
Pour cela nous ferrons des tests a partir du swager de fast api.


![img.png](imgs/ow00.png)
    

on vas manipuler par le biais de l'inspection du DOM les éléments d'authorisations


![img.png](imgs/ow02.png)

    
qui correspond a cette partie du code visible sur le DOM


![img.png](imgs/ow03.png)


Si on modifie le code sur le DOM en supprimant tout le code concernant le bouton comme l'image ci dessous


![img.png](imgs/ow05.png)


le resultats est toujours une erreur 403 sur la non authorisation


![img.png](imgs/ow06.png)



si on accede au formulaire pour l'identification par le mot de passe 


![img.png](imgs/ow01.png)


on pourra observer que dans l'input du formulaire nous ne pouvons pas modifier les authorisations



Conclusion je pense que nous respectons le point N°5 du référentiel OWASP



2 -
