from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project
from contributor.models import Contributor
from issue.models import Issue
from comment.models import Comment
from user.models import User
from .serializers import ProjectSerializer
from issue.serializers import IssueSerializer
from comment.serializers import CommentSerializer
from user.permissions import IsUserAuthenticated, IsContributor, IsAuthorOrReadOnly
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
