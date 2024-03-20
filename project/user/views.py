from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer
# from .permissions import IsUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsUser]

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        user = self.get_object()
        # récupère les noms de tous les projets auxquels l'utilisateur est associé en tant que contributeur.
        projects = user.contributor_set.all().values('project__name')
        return Response({"projects": projects})
