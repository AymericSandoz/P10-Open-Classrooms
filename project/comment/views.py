from rest_framework import viewsets
from .models import Comment
from user.models import User
from contributor.models import Contributor
from .serializers import CommentSerializer
from user.permissions import IsUserAuthenticated, IsContributor, IsAuthorOrReadOnly
from django.core.exceptions import ObjectDoesNotExist


class CommentViewSet(viewsets.ModelViewSet):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUserAuthenticated,
                          IsAuthorOrReadOnly, IsContributor]

    def get_queryset(self):
        """
        Surcharge de la méthode get_queryset pour retourner uniquement les commentaires
        des projets auxquels l'utilisateur actuel contribue.
        """
        user = self.request.user
        # Récupérer les IDs des projets auxquels l'utilisateur contribue
        contributor_projects_ids = Contributor.objects.filter(
            user=user).values_list('project', flat=True)
        # Filtrer les commentaires en fonction des projets auxquels l'utilisateur contribue
        return Comment.objects.filter(issue__project__id__in=contributor_projects_ids)

    def perform_create(self, serializer):
        try:
            user = User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            pass
        serializer.save(author=user)
