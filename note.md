C'est quoi une api REST ? Différence par rapport aux projet précédent.

C 'est quoi un ORM ?

C'est quoi un serializers ?

Explication du projet ?

je sais pas pourquoi je dois faire python manage.py makemigrations project
et non pas juste python manage.py makemigrations

# Lancer l'application

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
