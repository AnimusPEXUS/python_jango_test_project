

from _datetime import datetime

import django.contrib.auth.models
from django.core import mail
import django.db.models.signals
from django.dispatch.dispatcher import receiver
import django.http
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView, View
from django.contrib.messages import get_messages
from django.contrib import messages

from .models import Subscription, Post

import python_jango_test_project.settings


class UserHomeView(TemplateView):

    def get(self, request: django.http.HttpRequest):

        if not request.user.is_authenticated:
            messages.error(request, "not authenticated")
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
                'own_id': request.user.id,
                'messages': get_messages(request),
            }
        )

        return ret


class NewPost(View):
    template_name = 'new_post.html'

    def get(self, request: django.http.HttpRequest):

        if not request.user.is_authenticated:
            messages.error(request, "not authenticated")
            return django.http.HttpResponseRedirect("/login")

        ret = render(
            request,
            self.template_name,
            {
                'request': request,
                'messages': get_messages(request),
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
            messages.error(request, "not authenticated")
            return django.http.HttpResponseRedirect("/login")

        if not isinstance(pid, str):
            pid = int(pid)

        p = Post.objects.filter(id=pid).first()
        if p is None:
            messages.error(request, "post not found")
            return django.http.HttpResponseRedirect('/home')

        ret = render(
            request,
            self.template_name,
            {
                'p': p,
                'messages': get_messages(request),
            }
        )
        return ret


class LoginPost(View):

    def get(self, request):
        ret = render(
            request,
            'login.html',
            {
                'messages': get_messages(request),
            }
        )
        return ret

    def post(self, request):
        django.contrib.auth.login(
            request,
            request.POST['username'],
            request.POST['password']
        )
        return


def logout(req: django.http.HttpRequest) -> django.http.HttpResponse:
    django.contrib.auth.logout(req)
    return django.http.HttpResponseRedirect('/login')


@require_POST
def delete(req: django.http.HttpRequest) -> django.http.HttpResponse:

    pid = req.POST.get('pid', None)
    if pid is not None:
        pid = int(pid)

    if not req.user.is_authenticated:
        messages.error(req, "not authenticated")
        return HttpResponseRedirect("/home")

    p = Post.objects.filter(id=pid)
    if p is None:
        messages.error(req, "post not found")
        return HttpResponseRedirect("/home")

    for i in p:
        if i.user != req.user:
            messages.error(req, "not your post - can't delete")
            return HttpResponseRedirect("/home")

        i.delete()

    messages.info(req, "post deleted")

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

        if target_sub_user is None:
            messages.error(req, "no such user")
            return HttpResponseRedirect("/home")

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

        messages.info(req, "subscribed ok")

    else:

        messages.error(req, "not authenticated")

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

        if target_sub_user is None:
            messages.error(req, "no such user")
            return HttpResponseRedirect("/home")

        s = Subscription.objects.filter(
            user=req.user,
            subscription=target_sub_user
        )

        if s is not None:
            s.delete()

        messages.info(req, "unsubscribed ok")

    else:

        messages.error(req, "not authenticated")

    return HttpResponseRedirect("/home")


@receiver(django.db.models.signals.post_save)
def work_on_posts_actions_dave(sender, **kwargs):
    work_on_posts_actions_x('save', sender, **kwargs)


@receiver(django.db.models.signals.post_delete)
def work_on_posts_actions_delete(sender, **kwargs):
    work_on_posts_actions_x('dele', sender, **kwargs)


def work_on_posts_actions_x(act, sender, **kwargs):

    if not (python_jango_test_project.settings.
            PYTHON_JANGO_TEST_PROJECT_EMAIL_POSTING_ENABLED):
        return

    if sender != Post:
        return

    try:

        inst = kwargs.get('instance', None)
        if inst is None:
            return

        connection = mail.get_connection()

        subscribers = set()
        django.contrib.auth.models.User
        for i in django.contrib.auth.models.User.objects.all():
            for j in Subscription.objects.filter(subscription=inst.user):
                if j.user == i:
                    subscribers.add(i)

        if act == 'save':
            msg = mail.EmailMessage(
                '[sitename] {} created new topic: {}'.format(
                    inst.user.username,
                    inst.title,

                ),
                python_jango_test_project.settings.SITE_PREFIX +
                'view/' + str(i.id),
            )
        else:
            msg = mail.EmailMessage(
                '[sitename] topic deleted',
                python_jango_test_project.settings.SITE_PREFIX +
                'view/' + str(i.id),
            )

        for i in list(subscribers):
            if i.email != None:
                msg.to = [i.email]
                connection.send_messages([msg])
    except:
        pass
