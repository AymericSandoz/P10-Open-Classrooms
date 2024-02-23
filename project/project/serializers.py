from rest_framework import serializers
from .models import Contributor, User, Project, Issue, Comment
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
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'issue']


class IssueSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Issue
        fields = ['title', 'description',
                  'assigned_to', 'project', 'priority', 'tag', 'comments']

    def validate(self, data):
        contributor = data.get('assigned_to')
        project = data.get('project')

        if contributor and project and contributor not in project.contributors.all():
            raise serializers.ValidationError(
                "Le Contributor n'est pas un contributeur du Project")

        return data


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(
        many=True, read_only=True, required=False)
    issues = IssueSerializer(many=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'type', 'contributors', 'issues']
