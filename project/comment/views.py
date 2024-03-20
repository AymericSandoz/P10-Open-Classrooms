from rest_framework import viewsets
from .models import Comment
from user.models import User
from .serializers import CommentSerializer
from user.permissions import IsUserAuthenticated, IsContributor, IsAuthorOrReadOnly
from django.core.exceptions import ObjectDoesNotExist


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
