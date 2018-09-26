
from django.contrib import admin
import django.contrib.auth.views
from django.urls import path

import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',
         django.contrib.auth.views.LoginView.as_view(
             template_name="login.html")),
    path('logout', blog.views.logout),
    path('home', blog.views.UserHomeView.as_view()),
    path('new', blog.views.NewPost.as_view()),
    path('view/<int:pid>', blog.views.ViewPost.as_view()),
    path('delete', blog.views.delete),
    path('subscribe', blog.views.subscribe),
    path('unsubscribe', blog.views.unsubscribe),
]
