from rest_framework import serializers
from issue.models import Issue
from contributor.models import Contributor


class IssueSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Contributor.objects.all(), required=False)
    status = serializers.CharField(required=False)

    class Meta:
        model = Issue
        fields = ['title', 'description',
                  'assigned_to', 'project', 'priority', 'tag', 'status']

    def validate(self, data):
        contributor = data.get('assigned_to')
        project = data.get('project')

        # Vérifier que le Contributor est un contributeur du Project
        if contributor and project and contributor not in project.contributors.all():
            raise serializers.ValidationError(
                "Le Contributor que vous essayez d'assigner n'est pas un contributeur du Project")

        return data
