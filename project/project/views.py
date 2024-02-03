from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Contributor, User, Project
from .serializers import ContributorSerializer, UserSerializer, ProjectSerializer
from django.shortcuts import get_object_or_404


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

    @action(detail=True, methods=['post'])
    def link_to_project(self, request, pk=None):
        contributor = self.get_object()
        project_id = request.data.get('project_id')

        # Logique pour lier le contributeur au projet avec l'ID project_id
        project = get_object_or_404(Project, pk=project_id)

        contributor.projects.add(project)

        return Response({"status": "Contributeur lié au projet avec succès."})


class ProjectViewSet(viewsets.ViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
