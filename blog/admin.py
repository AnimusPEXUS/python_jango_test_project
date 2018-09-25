from django.contrib import admin

# Register your models here.
import blog.models

for i in [
    blog.models.Post,
    blog.models.Subscription,
    blog.models.Seen,
]:

    admin.site.register(i)
