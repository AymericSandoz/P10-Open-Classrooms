from rest_framework import serializers
from .models import Project
from contributor.serializers import ContributorSerializer
# from issue.serializers import IssueSerializer


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(
        many=True, read_only=True, required=False)
    # issues = IssueSerializer(many=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'type', 'contributors']  # , 'issues'
