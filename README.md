# Projet 10 OpenClassrooms: Créez une API sécurisée RESTful en utilisant Django REST

## Configuration et Installation

1. Clonez le dépôt: `git clone <url_du_dépôt>`
2. Naviguez vers le répertoire du projet: `cd projet`
3. Installez les dépendances avec `pipenv`: `pipenv install`
4. Activez l'environnement virtuel: `pipenv shell`
5. Appliquez les migrations: `python manage.py makemigrations` et `python manage.py migrate`
6. Lancez le serveur: `python manage.py runserver`

## Points d'accès API

- `/api/user/`: Point d'accès pour les opérations utilisateur
- `/api/project/`: Point d'accès pour les opérations de projet
- `/api/issue/`: Point d'accès pour les problèmes
- `/api/comment/`: Point d'accès pour les commentaires
- `/api/contributor/`: Point d'accès pour lier les projets aux utilisateurs

### actions spéciale

- `/api/project/assign_contributors/`: Permet d'assigner des contributeurs à un projet spécifique. Cette action utilise la méthode PATCH pour mettre à jour la liste des contributeurs du projet. Seul l'auteur du projet a accès à cette route.
- `/api/issue/change_status`: Permet de changer le statut d'une issue. Cette action utilise la méthode PATCH pour mettre à jour le statut de l'issue. Il faut être contributeur du projet de l'issue en question pour utiliser cette route.
- `/api/user/projects`: Récupère la liste des projets associés à un utilisateur. Cette action utilise la méthode GET pour obtenir les informations des projets.

## Permissions

- `IsAuthorOrReadOnly`: Seul l'auteur est autorisé ou les méthodes GET et HEAD
- `IsContributor`: Seuls les contributeurs d'un projet sont autorisés
- `IsUserAuthenticated`: Seuls les utilisateurs authentifiés sont autorisés
- `IsSelfOrReadOnly`: Seul les utilisateurs sont autorisés à modifier leurs propres données
- `IsAuthenticatedOrPostOnly`: Les utilisateurs non authentifiés ne peuvent que utiliser la méthode POST(en l'occurence ici se créer un compte utilisateur)
