from rest_framework import serializers
from .models import Contributor, User, Project, Issue
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "age", "password", "email",
                  "can_data_be_shared", "can_be_contacted"]

    def validate_password(self, value):
        """ hash the password before saving """
        return make_password(value)

    def validate(self, data):
        age = data.get('age')
        can_data_be_shared = data.get('can_data_be_shared')

        if can_data_be_shared and age < 15:
            raise serializers.ValidationError(
                'User must be at least 15 years old to share data.')

        return data


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'type']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
