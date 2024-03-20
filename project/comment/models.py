from django.db import models
import uuid
from issue.models import Issue
from user.models import User


class Comment(models.Model):
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_time = models.DateTimeField(auto_now_add=True)
