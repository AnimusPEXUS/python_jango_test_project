

from django import forms
import django.contrib.auth
import django.http
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView, View

from .forms import subscribe_button_form
from .models import Subscription, Post
from _datetime import datetime
from django.http.response import HttpResponseRedirect
from asyncio.log import logger
import logging


class UserHomeView(TemplateView):

    def get(self, request: django.http.HttpRequest):

        if not request.user.is_authenticated:
            return django.http.HttpResponseRedirect("/login")

        this_user_subscriptions = Subscription.objects.filter(
            user=request.user).all()

        subscribed_list = []

        for i in this_user_subscriptions:
            t = django.contrib.auth.models.User.objects.get(
                username=i.subscription.username)

            subscribed_list.append(t)

        posts = []
        for i in Post.objects.all():
            for j in subscribed_list:
                if i.user == j:
                    posts.append(i)

        posts.sort(key=lambda x: x.date)
        subscribed_list.sort(key=lambda x: x.username)

        ret = render(
            request,
            'user_homepage.html',
            {
                'posts': posts,
                'own_posts': Post.objects.filter(user=request.user).all(),
                'subscriptions': subscribed_list,
                'request': request,
                'subscribe_button_form': subscribe_button_form,
                'own_id': request.user.id,
            }
        )

        return ret


class NewPost(View):
    template_name = 'new_post.html'

    def get(self, request: django.http.HttpRequest):

        if not request.user.is_authenticated:
            return django.http.HttpResponseRedirect("/login")

        ret = render(
            request,
            self.template_name,
            {
                'request': request,
            }
        )
        return ret

    def post(self, request: django.http.HttpRequest):

        if request.user.is_authenticated:
            p = Post(user=request.user)
            p.title = request.POST['title']
            p.text = request.POST['text']
            p.date = datetime.utcnow()
            p.save()

        return django.http.HttpResponseRedirect('/home')


class ViewPost(TemplateView):
    template_name = 'view_post.html'

    def get(self, request: django.http.HttpRequest, pid):

        if not request.user.is_authenticated:
            return django.http.HttpResponseRedirect("/login")

        if not isinstance(pid, str):
            pid = int(pid)

        p = Post.objects.filter(id=pid).first()
        if p is None:
            return django.http.HttpResponseRedirect('/home')

        ret = render(
            request,
            self.template_name,
            {
                'p': p,
            }
        )
        return ret


class LoginPost(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        django.contrib.auth.login(
            request,
            request.POST['username'],
            request.POST['password']
        )
        return django.http.HttpResponseRedirect('/home')


def logout(req: django.http.HttpRequest) -> django.http.HttpResponse:
    django.contrib.auth.logout(req)
    return django.http.HttpResponseRedirect('/login')


@require_POST
def delete(req: django.http.HttpRequest) -> django.http.HttpResponse:

    pid = req.POST.get('pid', None)
    if pid is not None:
        pid = int(pid)

    if not req.user.is_authenticated:
        return HttpResponseRedirect("/home")

    p = Post.objects.filter(id=pid)
    if p is None:
        return HttpResponseRedirect("/home")

    for i in p:
        if i.user != req.user:
            return HttpResponseRedirect("/home")

        i.delete()

    return HttpResponseRedirect("/home")


@require_POST
def subscribe(req: django.http.HttpRequest) -> django.http.HttpResponse:

    uid = req.POST.get('uid', None)
    if uid is not None:
        uid = int(uid)

    username = req.POST.get('username', None)

    if req.user.is_authenticated:

        target_sub_user = None

        if username != None:
            u = django.contrib.auth.models.User.objects.filter(
                username=username).first()
            target_sub_user = u
        else:
            u = django.contrib.auth.models.User.objects.filter(
                id=uid).first()
            target_sub_user = u

        s = Subscription.objects.filter(
            user=req.user,
            subscription=target_sub_user
        ).first()

        if s is None:
            s = Subscription(
                user=req.user,
                subscription=target_sub_user
            )
            s.save()

    return HttpResponseRedirect("/home")


@require_POST
def unsubscribe(req: django.http.HttpRequest) -> django.http.HttpResponse:

    uid = req.POST.get('uid', None)
    if uid is not None:
        uid = int(uid)

    username = req.POST.get('username', None)

    if req.user.is_authenticated:

        target_sub_user = None

        if username != None:
            u = django.contrib.auth.models.User.objects.filter(
                username=username).first()
            target_sub_user = u
        else:
            u = django.contrib.auth.models.User.objects.filter(
                id=uid).first()
            target_sub_user = u

        s = Subscription.objects.filter(
            user=req.user,
            subscription=target_sub_user
        )

        if s is not None:
            s.delete()

    return HttpResponseRedirect("/home")
