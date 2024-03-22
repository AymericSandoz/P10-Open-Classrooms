from rest_framework import viewsets
from .models import Project
from contributor.models import Contributor
from user.models import User
from .serializers import ProjectSerializer
from user.permissions import IsUserAuthenticated, IsAuthorOrReadOnly
from django.core.exceptions import ObjectDoesNotExist


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
