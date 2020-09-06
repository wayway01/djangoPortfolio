from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Tag(models.Model):
    name = models.CharField(max_length = 32, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length = 32)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    is_public = models.BooleanField(default=True)
    date_posted = models.DateTimeField(default = timezone.now)
    date_updated = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    name = models.CharField(max_length = 255, default = "Anonymous")
    text = models.TextField()
    target = models.ForeignKey(Post, on_delete = models.CASCADE)
    date_created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.text[:20]


class Reply(models.Model):
    name = models.CharField(max_length = 255, default = "Anonymous")
    text = models.TextField()
    target = models.ForeignKey(Comment, on_delete = models.CASCADE)
    date_created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.text[:20]

