from django.db import models
from contributor.models import Contributor
from project.models import Project
from user.models import User


class Issue(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='issues')
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        Contributor, null=True, on_delete=models.CASCADE)
    priority_choices = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    priority = models.CharField(max_length=10, choices=priority_choices)
    tag_choices = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]
    tag = models.CharField(max_length=10, choices=tag_choices)
    status_choices = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    ]
    status = models.CharField(
        max_length=15, choices=status_choices, default='TODO')
    created_time = models.DateTimeField(auto_now_add=True)
