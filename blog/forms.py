
from django import forms


class PostForm(forms.Form):
    title = forms.TextInput()
    text = forms.Textarea()


class SubscribeForm(forms.Form):
    user = forms.IntegerField()


class UnSubscribeForm(forms.Form):
    user = forms.IntegerField()
