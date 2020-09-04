from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from cos.settings import LOGIN_URL
from webapp.models import Project
from django.http import HttpResponse

# Um decorotor permite filtrar quem tipo de user é que pode aceder á view!

# Este decorator serve para dar acesso unicamente aos cientistas!
def scientist_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_URL):
    '''
    Decorator para as views quer verifica se o utilizador esta logado como utilizador e cientista,
    redireciona para a pagina de login se necessario.
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
    Decorator para as views quer verifica se o utilizador esta logado como utilizador e donator,
    redireciona para a pagina de login se necessario.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.donator and u.donator.is_donator,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Este decorator serve para verificar se o utilizador é o dono do projeto!
def owner_required(func):
    '''
    Decorator para as views quer verifica se o utilizador cientista é dono do projeto,
    caso contrario redireciona para uma pagina com uma menssagem de erro!
    '''
    def check_and_call(request, *args, **kwargs):
        user = request.user
        pk = kwargs["pk"]
        project = Project.objects.get(pk=pk)
        if not (project.scientist.user.id == request.user.id):
            return HttpResponse("This project isn't yours ! Sorry, but not allowed !")
        return func(request, *args, **kwargs)
    return check_and_call
