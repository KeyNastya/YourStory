from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Chapter(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
