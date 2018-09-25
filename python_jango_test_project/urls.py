
from django.contrib import admin
from django.urls import path

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.UserHomeView.as_view()),
    path('new', views.NewPost.as_view()),
    path('view/<int:pid>', views.ViewPost.as_view()),
    path('subscribe/<int:uid>', views.subscribe),
    path('unsubscribe/<int:uid>', views.unsubscribe),
]
