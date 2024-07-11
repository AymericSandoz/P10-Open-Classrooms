from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'issue']

    def update(self, instance, validated_data):
        """ Il n'est pas possible de modifier l'issue d'un commentaire après sa création."""
        if 'issue' in validated_data:
            if validated_data['issue'] != instance.issue:
                raise serializers.ValidationError(
                    {'issue': ["Le champ Issue ne peut pas être modifié après la création du Commentaire."]})
            else:
                validated_data.pop('issue')

        return super().update(instance, validated_data)
