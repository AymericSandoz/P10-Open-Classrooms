from rest_framework import viewsets
from .models import Project
from contributor.models import Contributor
from user.models import User
from .serializers import ProjectSerializer
from user.permissions import IsUserAuthenticated, IsAuthorOrReadOnly
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsUserAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        try:
            user = User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            pass
        project = serializer.save(author=user)
        contributor = Contributor.objects.create(
            user=user, project=project)
        project.contributors.add(contributor)
        project.save()

    def get_queryset(self):
        # Renvoie uniquement les projets auxquels l'utilisateur est associé en tant que contributeur
        return Project.objects.filter(contributors__user=self.request.user)

    @action(detail=True, methods=['patch'])
    def assign_contributors(self, request, pk=None):
        """ Affecter des contributeurs à un projet."""
        project = get_object_or_404(Project, pk=pk)

        # Note : Je ne sais pas pourquoi mais la permission ISAuthorOrReadOnly ne fonctionne pas ici^^
        if project.author.id != request.user.id:
            return Response({'message': 'Seul l\'auteur du projet peut ajouter des contributeurs.'},
                            status=status.HTTP_403_FORBIDDEN)

        user_ids = request.data.get('users_ids')
        if not user_ids:
            return Response({'message': 'Aucun identifiant d\'utilisateur fourni.'}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(user_ids, int):
            user_ids = [user_ids]

        added_contributors = []
        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                # Vérifiez si l'utilisateur est déjà contributeur
                if not Contributor.objects.filter(user=user, project=project).exists():
                    Contributor.objects.create(user=user, project=project)
                    added_contributors.append(user_id)
            except User.DoesNotExist:
                continue

        return Response({'added_contributors': added_contributors}, status=status.HTTP_200_OK)
