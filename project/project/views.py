from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Contributor, User, Project, Issue, Comment
from .serializers import ContributorSerializer, UserSerializer, ProjectSerializer, IssueSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsUserAuthenticated, IsContributor, IsAuthorOrReadOnly, IsUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser]

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        user = self.get_object()
        # récupère les noms de tous les projets auxquels l'utilisateur est associé en tant que contributeur.
        projects = user.contributor_set.all().values('project__name')
        return Response({"projects": projects})


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsUserAuthenticated]

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        project = get_object_or_404(Project, pk=project_id)
        if project.author != self.request.user:
            raise PermissionDenied(
                "Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet.")
        contributor = serializer.save(project=project)
        project.contributors.add(contributor)
        project.save()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsUserAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        try:
            user = User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            pass
        project = serializer.save(author=user)  # Save the project first
        contributor = Contributor.objects.create(
            user=user, project=project)  # Then create the contributor
        # Add the contributor to the project
        project.contributors.add(contributor)
        project.save()  # Save the project again  # Save the author as a User

    # def get_queryset(self):
    #     # Renvoie uniquement les projets auxquels l'utilisateur est associé en tant que contributeur
    #     return Project.objects.filter(contributors__user=self.request.user)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsUserAuthenticated,
                          IsAuthorOrReadOnly, IsContributor]

    def perform_create(self, serializer):
        try:
            user = User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            pass
        serializer.save(author=user)

    @action(detail=True, methods=['update'])
    def change_status(self, request, pk=None):
        issue = self.get_object()
        status = request.data.get('status')

        # Logique pour changer le statut de l'issue
        issue.status = status
        issue.save()

        return Response({"status": "Statut de l'issue modifié avec succès."})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUserAuthenticated,
                          IsAuthorOrReadOnly, IsContributor]

    def perform_create(self, serializer):
        try:
            user = User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            pass
        serializer.save(author=user)
