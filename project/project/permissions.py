from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Project, Comment, Issue
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsUserAuthenticated(BasePermission):

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés
        return bool(request.user and request.user.is_authenticated)


class IsUser(BasePermission):
    def has_permission(self, request, view):
        # Seul le user peut modifier ou supprimer ses données
        if request.method in SAFE_METHODS:
            return True
        return request.user.id == int(view.kwargs.get('pk'))


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        # Si la requête est une requête POST
        if request.method == 'POST':
            # Récupérez le projet spécifié dans les données de la requête
            project_id = request.data.get('project')
            try:
                project = Project.objects.get(id=project_id)
            except ObjectDoesNotExist:
                return PermissionDenied(
                    "Le projet spécifié n'existe pas.")

            contributor_users = [
                contributor.user for contributor in project.contributors.all()]

            # L'utilisateur a la permission si il fait partie des contributeurs du projet
            return request.user in contributor_users

        # Pour les autres types de requêtes, autorisez l'accès
        return True

    def has_object_permission(self, request, view, obj):
        # Determine the project based on the type of obj
        if isinstance(obj, Comment):
            project = obj.issue.project
        elif isinstance(obj, Issue):
            project = obj.project
        elif isinstance(obj, Project):
            project = obj
        else:
            return False  # or handle other types as needed

        # Only the contributors of the project can access the object
        contributors_ids = [
            contributor.user.id for contributor in project.contributors.all()]
        return request.user.id in contributors_ids


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Seul l'auteur peut créer un contributeur
        if request.method == 'POST':
            project_id = request.data.get('project')
            try:
                project = Project.objects.get(id=project_id)
            except ObjectDoesNotExist:
                return PermissionDenied(
                    "Le projet spécifié n'existe pas.")
            return request.user.id == project.author.id
        else:
            return True

    def has_object_permission(self, request, view, obj):
        # Seul l'auteur de l'objet peut le modifier(Attentions has_object_permission ne marche pas pour Post et GETLIST)
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsContributorOrReadOnly(BasePermission):
    """
    Custom permission to only allow contributors of a project to create related objects.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        else:
            contributors_ids = [
                contributor.user.id for contributor in obj.contributors.all()]
        return request.user.id in contributors_ids
