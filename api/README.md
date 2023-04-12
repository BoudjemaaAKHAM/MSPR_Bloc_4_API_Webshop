## MSPR_Bloc_4
Repo git pour la mise en situation profesionnelle reconstituée du bloc de compétences 4.

creation de l'image dicker pour l'api:
docker build -t api:1.0.0 . 

demarage du conteneur : 
<!-- docker run -it --net=host --name api api:1.0.0 -->
docker run -it -p 9001:9001 --name api api:1.0.0

il faut aussi penser a mettre localhost ou 127.0.0.1 car avec windows cela ne marche pas forcement avec 0.0.0.0

<!-- docker run --detach --publish 8080:80 --name api api:1.0.0 -->

<!-- docker run --detach --publish 8081 --name api api:1.0.0 -->


pour obtenir l'addresse ip du conteneur:
docker exec -it api ip addr 

ip a l'epsi? : 192.168.65.4

## Constitution du groupe :
