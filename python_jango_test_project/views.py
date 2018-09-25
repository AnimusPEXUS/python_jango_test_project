

from django.views.generic.base import TemplateView


class UserHomeView(TemplateView):
    template_name = 'user_homepage.html'

    
class SubscribtionMng(TemplateView):
    template_name = 'subscribtion_mng.html'


class NewPost(TemplateView):
    template_name = 'write_new_post.html'
