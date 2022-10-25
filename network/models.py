from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, related_name="following", symmetrical=False)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/")
    bio = models.TextField(null=True, blank=True, max_length=264)
    nationality = models.CharField(null=True, blank=True, max_length=64)

class Post(models.Model):
    post = models.TextField()
    creator = models.CharField(max_length=64, blank=False)
    created = models.DateField(auto_now_add=False, auto_now=False, default=timezone.now)
    likes_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    
class Comment(models.Model):
    comment = models.TextField()
    creator = models.CharField(max_length=64, blank=False)
    created = models.DateField(auto_now_add=False, auto_now=False, default=timezone.now)
    original_post = models.PositiveIntegerField()
