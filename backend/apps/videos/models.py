from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='videos/')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
