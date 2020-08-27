from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from cos.settings import LOGIN_URL
from webapp.models import Project
from django.http import HttpResponse

# Um decorotor permite filtrar quem tipo de user é que pode aceder á view!

# Este decorator serve para dar acesso unicamente aos cientistas!


def scientist_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_URL):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.scientist and u.scientist.is_scientist,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Este decorator serve para dar acesso unicamente aos donators!


def donator_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_URL):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.donator and u.donator.is_donator,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def owner_required(func):
    def check_and_call(request, *args, **kwargs):
        user = request.user
        pk = kwargs["pk"]
        project = Project.objects.get(pk=pk)
        if not (project.scientist.user.id == request.user.id):
            return HttpResponse("It is not yours ! You are not permitted !")
        return func(request, *args, **kwargs)
    return check_and_call
