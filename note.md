C'est quoi une api REST ? Différence par rapport aux projet précédent.

C 'est quoi un ORM ?

C'est quoi un serializers ?

Explication du projet ?

je sais pas pourquoi je dois faire python manage.py makemigrations project
et non pas juste python manage.py makemigrations

# Lancer l'application

pipenv shell
cd project
python manage.py runserver

# créer un superuser

cd project
python manage.py createsuperuser

## Note sur le fonctionnement de l'appli

Je ne sais pas pourquoi mais je peux créer des token seulements aux users qui ont un password hashé -- En faite c'est normal c'est une bonne pratique de sécurité de django

Je ne trouve pas comment rentrer des headers dans l'interface fourni par DRF donc il faut utiliser des Postman...
aller dans headers
Rentrer authorization dans key
puis Bearer 'token' en value

MEttre paramètre page pour avoir page suivante
http://127.0.0.1:8000/api/user/?page=2

### créer un porjet dans postman

aller dans headers
Rentrer authorization dans key
puis Bearer 'token' en value

Dans body puis format json
{
"name": "Projet 1",
"description": "Description du projet 1",
"type": "frontend"
}

Question mentor :

Je ne comprends pas quand est ce que les contributors sont créer ?
A part à la création ou il y a un contbiteur de créer(l'auteur)
Car on ne peut pas créer d'issues et de commentaires si on est pas contributeurs.

La commande “curl”

Question mentor :

Méthod ela plus clean pour qu'un utilisateur puisse se créer un compte malgré les permissions

Le projet est découpé en plusieurs applications Django (packages) ;

La gestion et la mise à jour des dépendances sont assurées à l’aide d’un outil comme Pipenv ou Poetry ;

L’étudiant est capable d’expliquer les mesures de sécurité mises en place et en quoi elles respectent l’OWASP et le RGPD.

L’API est « green » si les conditions suivantes sont remplies :

Principe de green code mise en place :
Frugalité fonctionnelle :

Éliminer les fonctionnalités peu utilisées.

Optimisation du contenant :

Optimiser le code : ne garder que les bouts de code utilisé

Optimisation du contenu:
Pas d'image et de video

Réalisez un état des lieux
L’identification des fonctionnalités inutiles

Imbriquez les serializers pour la multiplication des requetes. Nottament quand je get un projet je get aussi ses issues et comments

Le listage des ressources est bridé par l’implémentation d’une pagination ;

Les requêtes se résolvent rapidement (un temps de réponse acceptable devrait être inférieur à 200 ms) ;

# Dernier truc à fix

Un user non connecter peut voir tous les users

A la création d'un projet il faut pouvoir tout rentrer

http://127.0.0.1:8000/api/issue/2/change_status/
