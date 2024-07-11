from rest_framework.permissions import BasePermission, SAFE_METHODS
from issue.models import Issue
from comment.models import Comment
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied


class IsUserAuthenticated(BasePermission):
    """ Permission personnalisée pour n'autoriser que les
    utilisateurs authentifiés à accéder à n'importe quelle ressource."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsSelfOrReadOnly(BasePermission):
    """ Permission personnalisée pour n'autoriser que l'utilisateur à accéder à ses propres données."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsContributor(BasePermission):
    """ Permission personnalisée pour n'autoriser que les contributeurs
    d'un projet à créer des issues ou des commentaires."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.data.get('issue'):
                issue_id = request.data.get('issue')
                try:
                    issue = Issue.objects.get(id=issue_id)
                except ObjectDoesNotExist:
                    return PermissionDenied(
                        "L'issue spécifiée n'existe pas.")
                project = issue.project
            elif request.data.get('comment'):
                comment_id = request.data.get('comment')
                try:
                    comment = Comment.objects.get(id=comment_id)
                except ObjectDoesNotExist:
                    return PermissionDenied(
                        "Le commentaire spécifié n'existe pas.")
                project = comment.issue.project
            else:
                return True

            contributor_users = [
                contributor.user for contributor in project.contributors.all()]

            return request.user in contributor_users

        else:
            return True


class IsAuthorOrReadOnly(BasePermission):
    """ Permission personnalisée pour n'autoriser que l'auteur à modifier ses propres ressources."""

    def has_object_permission(self, request, view, obj):
        # Seul l'auteur de l'objet peut le modifier(Attentions has_object_permission ne marche pas pour Post et GETLIST)
        # Seul l'auteur de l'objet peut le modifier sauf dans le cas d'un changement de statut d'une issue.
        if request.method in SAFE_METHODS or view.action == 'change_status':
            return True
        return obj.author == request.user


class IsAuthenticatedOrPostOnly(BasePermission):
    """ Permission personnalisée pour n'autoriser les users non authentifiés qu'à se créer un compte."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return bool(request.user and request.user.is_authenticated)
