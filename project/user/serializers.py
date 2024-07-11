from rest_framework import serializers
from user.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "age", "password", "email",
                  "can_data_be_shared", "can_be_contacted"]

    def validate_password(self, value):
        """ hash le mdp avant de l'enregistrer"""
        password_validation.validate_password(value)
        return make_password(value)

    def validate(self, data):
        age = data.get('age')
        can_data_be_shared = data.get('can_data_be_shared')

        if can_data_be_shared and age < 15:
            raise serializers.ValidationError(
                'User must be at least 15 years old to share data.')

        return data

    def to_representation(self, instance):
        """Affiche tous les champs si l'utilisateur à représenter est l'utilisateur connecté,
          sinon seulement username et email."""
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user == instance:
            # Si l'utilisateur connecté est le même que celui à représenter, retourner tous les champs.
            return ret
        else:
            # Sinon, retourner uniquement username et email.
            return {"username": ret["username"], "email": ret["email"]}
