from django.db import models
from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone


class Comedian(models.Model):
    name = models.CharField(max_length=30)
    followers = models.ManyToManyField(User)
    # followed = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(null=True)
    tickets = models.URLField(max_length=100)
    description = models.CharField(max_length=300)
    comedian = models.ForeignKey(Comedian ,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    likers = models.ManyToManyField(User, related_name="likers")
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    pubdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_text