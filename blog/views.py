

import django.http
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView

import django.contrib.auth

from .models import Subscription
from .forms import PostForm
from django.shortcuts import render


class UserHomeView(TemplateView):
    template_name = 'user_homepage.html'

    def __str__(
            self,
            req: django.http.HttpRequest,
    ):

        return


class NewPost(TemplateView):
    template_name = 'new_post.html'

    def __str__(self, req: django.http.HttpRequest):
        if req.method == "POST":
            form = PostForm(req.POST)
        else:
            form = PostForm

        self.form = form

        return


class ViewPost(TemplateView):
    template_name = 'view_post.html'

    def __str__(
            self,
            req: django.http.HttpRequest,
    ):
        pass


def logout(req: django.http.HttpRequest) -> django.http.HttpResponse:
    django.contrib.auth.logout(req)


@require_http_methods(["POST"])
def subscribe(
        req: django.http.HttpRequest,
        uid: int,
) -> django.http.HttpResponse:

    if req.user.is_authenticated():
        Subscription.objects.get_or_create(
            whos=req.user,
            who=uid
        )


@require_http_methods(["POST"])
def unsubscribe(
        req: django.http.HttpRequest,
        uid: int,
) -> django.http.HttpResponse:

    if req.user.is_authenticated():
        Subscription.objects.filter(
            whos=req.user,
            who=uid
        ).delete()
