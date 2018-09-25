

import django.http
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView

from .models import Subscription


class UserHomeView(TemplateView):
    template_name = 'user_homepage.html'

    def __str__(
            self,
            req: django.http.HttpRequest, 
            ):
        pass
    

class NewPost(TemplateView):
    template_name = 'new_post.html'

    def __str__(
            self,
            req: django.http.HttpRequest, 
            ):
        pass

class ViewPost(TemplateView):
    template_name = 'view_post.html'
    
    def __str__(
            self,
            req: django.http.HttpRequest, 
            ):
        pass


@require_http_methods(["POST"])
def subscribe(
        req: django.http.HttpRequest,
        uid: int,
        ) -> django.http.HttpResponse:
    
    current_user_uid = 123  # TODO
    
    Subscription.objects.get_or_create(whos=current_user_uid, who=uid)


@require_http_methods(["POST"])
def unsubscribe(
        req: django.http.HttpRequest,
        uid: int,
        ) -> django.http.HttpResponse:
    current_user_uid = 123  # TODO
    
    Subscription.objects.filter(whos=current_user_uid, who=uid).delete()
