from django.db import models
from django.utils import timezone

from authApp.models import User

# Create your models here.


class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class StoryView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_seen = timezone.now()
        return super(StoryView, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} viewed \"{self.story.title}\""
