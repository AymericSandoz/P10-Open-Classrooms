from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from issue.models import Issue
from user.models import User
from contributor.models import Contributor
from .serializers import IssueSerializer
from user.permissions import IsUserAuthenticated, IsContributor, IsAuthorOrReadOnly
from django.core.exceptions import ObjectDoesNotExist


class IssueViewSet(viewsets.ModelViewSet):
    # queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsUserAuthenticated,
                          IsAuthorOrReadOnly, IsContributor]

    def get_queryset(self):
        """
        Surcharge de la méthode get_queryset pour retourner uniquement les issues
        des projets auxquels l'utilisateur actuel contribue.
        """
        user = self.request.user
        # Récupérer les IDs des projets auxquels l'utilisateur contribue
        contributor_projects_ids = Contributor.objects.filter(
            user=user).values_list('project', flat=True)
        # Filtrer les issues en fonction des projets auxquels l'utilisateur contribue
        return Issue.objects.filter(project__id__in=contributor_projects_ids)

    def perform_create(self, serializer):
        try:
            user = User.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            pass
        serializer.save(author=user)

    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        issue = self.get_object()
        status = request.data.get('status')

        issue.status = status
        issue.save()

        return Response({"status": "Statut de l'issue modifié avec succès."})
