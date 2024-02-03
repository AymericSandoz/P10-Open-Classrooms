from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Contributor, User, Project, Issue
from .serializers import ContributorSerializer, UserSerializer, ProjectSerializer, IssueSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAdminAuthenticated, IsUserAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        user = self.get_object()
        # récupère les noms de tous les projets auxquels l'utilisateur est associé en tant que contributeur.
        projects = user.contributor_set.all().values('project__name')
        return Response({"projects": projects})


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    # permission_classes = [IsUserAuthenticated]

    @action(detail=True, methods=['post'])
    def link_to_project(self, request, pk=None):
        contributor = self.get_object()
        project_id = request.data.get('project_id')

        # Logique pour lier le contributeur au projet avec l'ID project_id
        project = get_object_or_404(Project, pk=project_id)

        contributor.projects.add(project)

        return Response({"status": "Contributeur lié au projet avec succès."})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsUserAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        contributor, created = Contributor.objects.get_or_create(user=user)
        project = serializer.save(author=contributor)
        project.contributors.add(contributor)
        project.save()


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    # permission_classes = [IsUserAuthenticated]

    @action(detail=True, methods=['update'])
    def change_status(self, request, pk=None):
        issue = self.get_object()
        status = request.data.get('status')

        # Logique pour changer le statut de l'issue
        issue.status = status
        issue.save()

        return Response({"status": "Statut de l'issue modifié avec succès."})
