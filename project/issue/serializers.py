from rest_framework import serializers
from issue.models import Issue
from comment.serializers import CommentSerializer


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
