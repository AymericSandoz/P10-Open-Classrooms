from rest_framework import serializers
from .models import Contributor, User, Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["age"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
