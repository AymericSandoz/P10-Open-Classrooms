from rest_framework import viewsets
from .models import Contributor
from iproject.models import Project
from .serializers import ContributorSerializer
from django.shortcuts import get_object_or_404
from user.permissions import IsUserAuthenticated
from rest_framework.exceptions import PermissionDenied


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
