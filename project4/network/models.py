from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class NewPost(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

class UserPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    followed = models.BooleanField(default=False)

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    user_page = models.ForeignKey(UserPage, on_delete=models.RESTRICT, null=True)