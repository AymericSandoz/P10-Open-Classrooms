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

    def update(self, instance, validated_data):
        # Il n'est pas possible de modifier le project d'une issue après sa création
        if 'project' in validated_data:
            # Si le project dans validated_data est différent de celui déjà associé à l'instance
            if validated_data['project'] != instance.project:
                raise serializers.ValidationError(
                    {'project': ["Le champ Project ne peut pas être modifié après la création de l'Issue."]})
            else:
                # Si le project est le même, on le retire de validated_data pour éviter une mise à jour inutile
                validated_data.pop('project')

        return super().update(instance, validated_data)
