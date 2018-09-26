
from django.template import loader


def subscribe_button_form(
    uid: int=None,
    username: str=None,
    un: bool=False,
    edit: bool=False,
    prompt: bool=False,
    request=None,
):
    un_v = ''
    if un:
        un_v = 'un'

    ret = loader.render_to_string(
        'subscribe_form.html',
        context={
            'un_v': un_v,
            'uid': uid,
            'username': username,
            'edit': edit,
            'prompt': prompt,
        },
        request=request,
    )

    return ret
