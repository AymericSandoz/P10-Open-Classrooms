from django.urls import path, include
from rest_framework import routers
from .views import CommentViewSet

router = routers.SimpleRouter()
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
