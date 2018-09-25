
from django.db import models


class Post(models.Model):
    whos = models.IntegerField()  # who's post
    date = models.DateTimeField() 
    title = models.TextField() 
    text = models.TextField()
    
    
class Subscription(models.Model):
    whos = models.IntegerField()  # who is subscribed
    who = models.IntegerField()  # on who


class Seen(models.Model):
    who = models.IntegerField()  # who's memory
    what = models.IntegerField()  # post to mark seen
