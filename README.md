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

## Points d'accès API spécifiques

### Assignation de contributeurs à un projet

- **Endpoint**: `/api/project/assign_contributors/`
- **Méthode**: PATCH
- **Description**: Permet d'assigner des contributeurs à un projet spécifique. Cette action met à jour la liste des contributeurs du projet.
- **Accès**: Réservé exclusivement à l'auteur du projet.
- **Variables requises**:
  - `users_ids`: Array - Identifiants des utilisateurs à ajouter au projet.

### Changement de statut d'une issue

- **Endpoint**: `/api/issue/change_status`
- **Méthode**: PATCH
- **Description**: Permet de changer le statut d'une issue. Cette action met à jour le statut de l'issue concernée.
- **Accès**: Disponible uniquement pour les contributeurs du projet associé à l'issue.
- **Variables requises**:
  - `status`: String - Le nouveau statut de l'issue. Valeurs possibles : ["To Do", "In Progress", "Finished"].

### Récupération des projets associés à un utilisateur

- **Endpoint**: `/api/user/projects`
- **Méthode**: GET
- **Description**: Récupère la liste des projets auxquels un utilisateur contribue.
- **Accès**: Ouvert à tous les utilisateurs authentifiés souhaitant consulter les projets auxquels ils contribuent.

## Permissions

- `IsAuthorOrReadOnly`: Seul l'auteur est autorisé ou les méthodes GET et HEAD
- `IsContributor`: Seuls les contributeurs d'un projet sont autorisés
- `IsUserAuthenticated`: Seuls les utilisateurs authentifiés sont autorisés
- `IsSelfOrReadOnly`: Seul les utilisateurs sont autorisés à modifier leurs propres données
- `IsAuthenticatedOrPostOnly`: Les utilisateurs non authentifiés ne peuvent que utiliser la méthode POST(en l'occurence ici se créer un compte utilisateur)

## Modèles de données

### Comment

- `text` (string, obligatoire): Le texte du commentaire.
- `issue` (integer, obligatoire): L'identifiant de l'issue associée au commentaire.

### Contributor

- `id` (integer, en lecture seule): L'identifiant unique du contributeur.
- `project` (integer, obligatoire): L'identifiant du projet associé.
- `user` (integer, obligatoire): L'identifiant de l'utilisateur associé.
- `created_time` (string, format date-time, en lecture seule): La date et l'heure de création du contributeur.

### Issue

- `title` (string, obligatoire): Le titre de l'issue.
- `description` (string, obligatoire): La description de l'issue.
- `assigned_to` (integer, optionnel): L'identifiant de l'utilisateur auquel l'issue est assignée.
- `project` (integer, obligatoire): L'identifiant du projet associé.
- `priority` (string, obligatoire): La priorité de l'issue. Valeurs possibles: [ LOW, MEDIUM, HIGH ].
- `tag` (string, obligatoire): Le tag de l'issue. Valeurs possibles: [ BUG, FEATURE, TASK ].
- `status` (string, optionnel): Le statut de l'issue. Valeurs possibles : [To
  Do, In Progress, Finished]

### Project

- `name` (string, obligatoire): Le nom du projet.
- `description` (string, obligatoire): La description du projet.
- `type` (string, obligatoire): Le type du projet. Valeurs possibles: [ backend, frontend, ios, android ].
- `contributors` (array, en lecture seule): La liste des contributeurs associés au projet.

### TokenObtainPair

- `username` (string, obligatoire): Le nom d'utilisateur.
- `password` (string, obligatoire): Le mot de passe.

### TokenRefresh

- `refresh` (string, obligatoire): Le token de rafraîchissement.
- `access` (string, en lecture seule): Le token d'accès.

### User

- `username` (string, obligatoire): Le nom d'utilisateur.
- `age` (integer, obligatoire): L'âge de l'utilisateur.
- `password` (string, obligatoire): Le mot de passe.
- `email` (string, format email, optionnel): L'adresse email de l'utilisateur.
- `can_data_be_shared` (boolean, optionnel): Si l'utilisateur autorise le partage de ses données.
- `can_be_contacted` (boolean, optionnel): Si l'utilisateur accepte d'être contacté.
