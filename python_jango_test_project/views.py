

from django.views.generic.base import TemplateView


class UserHomeView(TemplateView):
    template_name = 'user_homepage.html'

    
class SubscribtionMng(TemplateView):
    template_name = 'subscribtion_mng.html'


class NewPost(TemplateView):
    template_name = 'new_post.html'


class ViewPost(TemplateView):
    template_name = 'view_post.html'


def subscribe(req):
    pass


def unsubscribe(req):
    pass
