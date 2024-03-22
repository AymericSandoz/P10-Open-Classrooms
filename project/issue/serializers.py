from rest_framework import serializers
from issue.models import Issue
from user.models import User


class IssueSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False)

    class Meta:
        model = Issue
        fields = ['title', 'description',
                  'assigned_to', 'project', 'priority', 'tag']


def create(self, validated_data):
    author_username = validated_data.pop('author')
    author, created = User.objects.get_or_create(username=author_username)
    issue = Issue.objects.create(author=author, **validated_data)
    return issue


def validate(self, data):
    contributor = data.get('assigned_to')
    project = data.get('project')

    if contributor and project and contributor not in project.contributors.all():
        raise serializers.ValidationError(
            "Le Contributor n'est pas un contributeur du Project")

    return data
