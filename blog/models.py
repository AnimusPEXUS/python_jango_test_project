
from django.db import models

import django.contrib.auth.models


class Post(models.Model):
    user = models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=models.CASCADE
    )

    date = models.DateTimeField()
    title = models.TextField()
    text = models.TextField()


class Subscription(models.Model):
    user = models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=models.CASCADE,
        related_name="use",
    )

    subscription = models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=models.CASCADE,
    )


class Seen(models.Model):
    user = models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=models.CASCADE
    )

    posts =  models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )