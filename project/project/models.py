from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)
    age = models.PositiveIntegerField()

    def clean(self):
        if self.age < 15 and self.can_data_be_shared:
            raise ValidationError(
                "User must be at least 15 years old to share data")
        super().clean()


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Project(models.Model):
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    type_choices = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('ios', 'iOS'),
        ('android', 'Android'),
    ]
    type = models.CharField(max_length=10, choices=type_choices)


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(Contributor, on_delete=models.CASCADE)
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


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    link_to_issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name='comments')
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_time = models.DateTimeField(auto_now_add=True)


class Test(models.Model):
    test = models.CharField(max_length=255)
