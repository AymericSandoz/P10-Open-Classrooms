# Projet 10 OpenClassrooms: Créez une API sécurisée RESTful en utilisant Django REST

## Configuration et Installation

1. Clonez le dépôt: `git clone <url_du_dépôt>`
2. Naviguez vers le répertoire du projet: `cd projet`
3. Installez les dépendances: `pip install -r requirements.txt`
4. Appliquez les migrations: `python manage.py makemigrations` et `python manage.py migrate`
5. Lancez le serveur: `python manage.py runserver`

## Points d'accès API

- `/api/user/`: Point d'accès pour les opérations utilisateur
- `/api/project/`: Point d'accès pour les opérations de projet
- `/api/issue/`: Point d'accès pour les problèmes
- `/api/comment/`: Point d'accès pour les commentaires
- `/api/contributor/`: Point d'accès pour lier les projets aux utilisateurs

## Permissions

- `IsAuthorOrReadOnly`: Seul l'auteur est autorisé ou les méthodes GET et HEAD
- `IsContributor`: Seuls les contributeurs d'un projet sont autorisés
- `IsUserAuthenticated`: Seuls les utilisateurs authentifiés sont autorisés
- `IsAdminAuthenticated`: Seuls les administrateurs authentifiés sont autorisés
