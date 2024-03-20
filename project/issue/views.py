from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from issue.models import Issue
from user.models import User
from .serializers import IssueSerializer
from user.permissions import IsUserAuthenticated, IsContributor, IsAuthorOrReadOnly
from django.core.exceptions import ObjectDoesNotExist


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
