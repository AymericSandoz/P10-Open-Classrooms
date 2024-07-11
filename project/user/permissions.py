from rest_framework.permissions import BasePermission, SAFE_METHODS
from issue.models import Issue
from comment.models import Comment
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied


# class IsAdminAuthenticated(BasePermission):

#     def has_permission(self, request, view):
#         # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
#         return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsUserAuthenticated(BasePermission):
    """ Permission personnalisée pour n'autoriser que les utilisateurs authentifiés à accéder à une ressource."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsSelfOrReadOnly(BasePermission):
    """ Permission personnalisée pour n'autoriser que l'utilisateur à accéder à ses propres données."""

    def has_object_permission(self, request, view, obj):
        # Seul l'utilisateur peut modifier ses propres données
        if request.method in SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsContributor(BasePermission):
    """ Permission personnalisée pour n'autoriser que les contributeurs d'un projet à accéder à ses ressources."""

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

            contributor_users = [
                contributor.user for contributor in project.contributors.all()]

            # L'utilisateur a la permission si il fait partie des contributeurs du projet
            return request.user in contributor_users

        else:
            return True

    # def has_object_permission(self, request, view, obj):
    #     # Determine the project based on the type of obj
    #     if isinstance(obj, Comment):
    #         project = obj.issue.project
    #     elif isinstance(obj, Issue):
    #         project = obj.project
    #     elif isinstance(obj, Project):
    #         project = obj
    #     else:
    #         return False

    #     # Only the contributors of the project can access the object
    #     contributors_ids = [
    #         contributor.user.id for contributor in project.contributors.all()]
    #     return request.user.id in contributors_ids


class IsAuthorOrReadOnly(BasePermission):
    """ Permission personnalisée pour n'autoriser que l'auteur à modifier ses propres ressources."""

    # def has_permission(self, request, view):
    #     if request.method == 'POST':
    #         project_id = request.data.get('project')
    #         try:
    #             project = Project.objects.get(id=project_id)
    #         except ObjectDoesNotExist:
    #             return PermissionDenied(
    #                 "Le projet spécifié n'existe pas.")
    #         return request.user.id == project.author.id
    #     else:
    #         return True

    def has_object_permission(self, request, view, obj):
        # Seul l'auteur de l'objet peut le modifier(Attentions has_object_permission ne marche pas pour Post et GETLIST)
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


# class IsContributorOrReadOnly(BasePermission):
#     """
#     Custom permission to only allow contributors of a project to create related objects.
#     """

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True

#         else:
#             contributors_ids = [
#                 contributor.user.id for contributor in obj.contributors.all()]
#         return request.user.id in contributors_ids


class IsAuthenticatedOrPostOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return bool(request.user and request.user.is_authenticated)
