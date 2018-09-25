
from django.db import models

import django.contrib.auth.models


class Post(models.Model):
    whos = models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=models.CASCADE
        )  

    date = models.DateTimeField() 
    title = models.TextField() 
    text = models.TextField()
    
    
class Subscription(models.Model):
    whos = models.ForeignKey(
        django.contrib.auth.models.User,        
        on_delete=models.CASCADE,
        related_name="user",
        ) 

    who = models.ManyToManyField(
        django.contrib.auth.models.User
        ) 


class Seen(models.Model):
    whos = models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=models.CASCADE
        ) 

    what = models.ManyToManyField(
        Post
        ) 
