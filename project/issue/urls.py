from django.urls import path, include
from rest_framework import routers
from .views import IssueViewSet
router = routers.SimpleRouter()
router.register('issue', IssueViewSet, basename='issue')

urlpatterns = [
    path('', include(router.urls)),
]
