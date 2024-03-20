from django.db import models
from user.models import User
from contributor.models import Contributor


class Project(models.Model):
    author = models.ForeignKey(
        User, related_name='authored_projects', on_delete=models.CASCADE)
    contributors = models.ManyToManyField(
        Contributor, related_name='contributed_to_projects')
    name = models.CharField(max_length=255)
    description = models.TextField()
    type_choices = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('ios', 'iOS'),
        ('android', 'Android'),
    ]
    type = models.CharField(max_length=10, choices=type_choices)
    created_time = models.DateTimeField(auto_now_add=True)
