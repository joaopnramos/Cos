from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from .decorators import scientist_required, donator_required, owner_required
from webapp import models
from .serializers import DataSerializer, ProjectSerializer, DataGiveSerializer
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import tokengenerator
from rest_framework.permissions import IsAuthenticated
from cos.settings import DOWNLOAD_DIR
import os


# Start View
class RegisterView(TemplateView):
    """ Pagina inicial do projeto """

    template_name = "webapp/generic_register.html"

# Registro do Cientista!!


def scietist_register(request):
    """ View destinada ao registo do cientista """

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        scientist_form = ScientistForm(data=request.POST)
        if user_form.is_valid() and scientist_form.is_valid():
            emails = user_form.cleaned_data.get("email")
            first_name = scientist_form.cleaned_data.get("first_name")
            last_name = scientist_form.cleaned_data.get("last_name")
            phone = scientist_form.cleaned_data.get("phone")
            address = scientist_form.cleaned_data.get("address")
            work_local = scientist_form.cleaned_data.get("work_local")
            bi = scientist_form.cleaned_data.get("bi")
            bis = Scientist.objects.order_by("bi")

            for u in bis:
                if bi == u.bi:
                    return messages.error(request, 'This bi already exists!')
            if 10000000 < bi < 99999999 and 90000000 < phone < 999999999:
                scientist_profile = Scientist(
                    first_name=first_name, last_name=last_name, address=address, work_local=work_local, bi=bi, phone=phone, email=emails)
                user = user_form.save()
                user.set_password(user.password)
                user.is_active = False
                user.save()
                scientist_profile.user = user
                scientist_profile.save()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse("activate", kwargs={
                               "uidb64": uidb64, "token": tokengenerator.make_token(user)})
                email_subject = "Activate you accounts"
                activate_url = "http://" + domain+link
                email_body = "Hi" + first_name + " " + last_name + \
                    "Please use this link to verify the account\n" + activate_url
                email = EmailMessage(
                    email_subject, email_body, "noreply@semycolon.com", [emails],)
                email.send(fail_silently=False)

                registered = True

            else:
                messages.error(request, 'Phone number or bi are wrong!')

        else:
            print(user_form.errors, scientist_form.errors)
    else:
        user_form = UserForm
        scientist_form = ScientistForm

    return render(request, "webapp/registration_scientist.html",
                  {"user_form": user_form,
                   "scientist_form": ScientistForm,
                   "registered": registered})

# Registro do donator!


def donator_register(request):
    """ View destinada ao registo do donator """

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        donator_form = DonatorForm(data=request.POST)
        if user_form.is_valid() and donator_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            age = donator_form.cleaned_data.get("age")
            email = user_form.cleaned_data.get("email")
            donator_profile = Donator(age=age, email=email)
            donator_profile.user = user
            donator_profile.save()
            registered = True
        else:
            print(user_form.errors, donator_form.errors)
    else:
        user_form = UserForm
        donator_form = DonatorForm

    return render(request, "webapp/registration_donator.html",
                  {"user_form": user_form,
                   "donator_form": donator_form,
                   "registered": registered})

# Login generalista


def user_login(request):
    """ Login generalista, este login serve tanto para os donators como para os cientistas """

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            messages.error(request, 'username or password are incorrect')
            return redirect('user_login')
    else:
        form = AuthenticationForm()
        return render(request, "webapp/login.html", {'form': form})

# Logout!


@login_required
def user_logout(request):
    """ Permite fazer o logout """
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# View que permite a criação de um projeto!


@scientist_required
@login_required
def ProjectCreateView(request):
    """ View que permite ao cientista criar um projeto """

    if request.method == "POST":
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid:
            if request.user:
                project = project_form.save(commit=False)
                project.owner = request.user.scientist.id
                project.scientist = request.user.scientist
                project.save()
                ids = project.id
                messages.success(request, "Project created")
                return redirect('webapp:detail', pk=ids)
        else:
            print(project_form.errors)
    else:
        project_form = ProjectForm
    return render(request, "webapp/project_form.html", {"form": project_form})

# Demonstra uma lista de todos os proejetos aos cientistas


@method_decorator([login_required, scientist_required], name='dispatch')
class ProjectListView(ListView):
    """ Esta vista serve para ver todos os projeto """
    context_object_name = "projects"
    model = models.Project

# Serve para demonstrar os detalhes de um projeto


@method_decorator([login_required], name='dispatch')
class ProjectDetailView(DetailView):
    """ Esta view serve para ver os detalhes do projeto """
    context_object_name = "project"
    model = models.Project
    template_name = "webapp/project_detail.html"

# Serve para atulizar um projeto e só está disponivel para os cientistas e para os donos no projeto


@method_decorator([login_required, scientist_required, owner_required], name='dispatch')
class ProjectUpdateView(UpdateView):
    """ Esta view serve para atualizar o projeto """
    model = models.Project
    fields = ("name", "description", "sensorsChoice", "periodChoice", "spacetimeChoice")
    success_url = reverse_lazy('webapp:list')

# Serve para apagar um projeto


@method_decorator([login_required, scientist_required, owner_required], name='dispatch')
class ProjectDeleteView(DeleteView):
    """ Esta view serve para apagar um projeto """
    model = models.Project
    success_url = reverse_lazy("webapp:list")

# Faz a entrada de um donator num projeto


def DataGiveView(request, pk):
    """ Cria o objeto DataGive, ou seja, a partir da criação deste objeto o donator faz parte do projeto"""

    pro =  Project.objects.filter(id=pk)
    for pr in pro:
        if pr.finished:
            return redirect("webapp:myDprojects")

    if DataGive.objects.filter(project=pk).filter(donator=request.user.donator.id).exists():
        """ Serve para verificar se o donator ja faz parte do projeto e se sim ir para a detailview do mesmo """

        pks = str(pk)
        return HttpResponseRedirect("mydonatorprojects/" + pks)

    in_project = False
    if request.method == "POST":
        """ Criação do objeto DataGive """
        project = get_object_or_404(Project, pk=pk)
        donator = request.user.donator
        datagive = DataGive(project=project, donator=donator)
        datagive.save()
        in_project = True
    return render(request, "webapp/project_registry.html", {"in_project": in_project})

# Lista de todos projetos existentes disponiveis para o donator


@login_required
@donator_required
def DonatorList(request):
    """ Lista de todos os projetos do donator """

    pd_list = Project.objects.filter(finished=False).order_by("name")

    return render(request, "webapp/project_donator_list.html", context={"pd_list": pd_list})

# Profile


@login_required
@scientist_required
def profileScientist(request):
    """ Perfil do cientista """

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/webapp/profile/')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {'u_form': u_form}
    return render(request, 'webapp/profile.html', context)

# Projetos dos proprios cientistas


@login_required
@scientist_required
def privateScientistProjectView(request):
    """ Vista dos proprios projetos dos cientistas """
    context = {}
    user_id = request.user.scientist.id
    projects_list = Project.objects.filter(owner=user_id)
    context["data"] = projects_list
    return render(request, "webapp/privateprojects.html", context)

# Projetos de quais o donator faz parte


@login_required
@donator_required
def privateDonatorProjectView(request):
    """ Vista dos projetos de qual o donator faz parte """
    context = {}
    pj_list = []
    user = request.user.donator
    datagive_objects = DataGive.objects.filter(donator=user)
    for pj in datagive_objects:
        pj_list.append(pj.project)

    context["data"] = pj_list
    context["leave"] = True

    return render(request, "webapp/privateprojects.html", context)

# Serve para os cientistas finalizarem os projetos


@login_required
@scientist_required
def finishthedproject(request, pk):
    """ Permite ao cientista finalizar o projeto """
    project = get_object_or_404(Project, pk=pk)
    project.project_finished()
    project.save()
    pks = str(pk)
    return HttpResponseRedirect(reverse("index"))

# Rest Api end point do model Data


class DataViewSet(ModelViewSet):
    """ Permite adicionar dados aos projetos """

    serializer_class = DataSerializer
    queryset = models.Data.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

# Rest Api end point do model Project


class ProjectViewSet(ModelViewSet):
    """ Permite adicionar projetos através de gson, basicamente é um end point """

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

# Rest Api end point do model DataGive


class DataGiveViewSet(ModelViewSet):
    """ Permite adicionar dados aos projetos através de gson, basicamente é um end point """

    serializer_class = DataGiveSerializer
    queryset = DataGive.objects.filter(givingFinished=False)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("donator",)

# Verificação do token


class Verification(View):
    """ Esta view serve para fazer a verificação da conta através
        to token enviado por email """

    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not tokengenerator.check_token(user, token):
                return redirect("login" + "?message=" + "User already activated")

            if user.is_active:
                return redirect("user_login")

            user.is_active = True
            user.save()
            messages.success(request, "Account activated sucessfully")

        except Exception as ex:
            pass
        return redirect("user_login")

# Projetos ativos cientista


def MyActiveProjectsD(request):
    """ View que demonstra os projetos ativos do utilizador donator  """
    context = {}
    pj_list = []
    user = request.user.donator
    datagive_objects = DataGive.objects.filter(
        givingFinished=False).filter(donator=user)
    for pj in datagive_objects:
        pj_list.append(pj.project)

    context["data"] = pj_list
    context["Finalized"] = False

    return render(request, "webapp/privateprojects.html", context)

# Projetos arquivados Donator


def MyArchivedProjectsD(request):
    """ View que demonstra os projetos arquivados do utilizador donator  """
    context = {}
    pj_list = []
    user = request.user.donator
    datagive_objects = DataGive.objects.filter(
        givingFinished=True).filter(donator=user)
    for pj in datagive_objects:
        pj_list.append(pj.project)

    context["data"] = pj_list
    context["Finalized"] = True
    return render(request, "webapp/privateprojects.html", context)

# Projetos ativos Cientista


def MyActiveProjectsS(request):
    """ View que demonstra os projetos ativos do utilizador  """
    context = {}
    pj_list = []

    user = request.user.scientist
    scientist_objects = Project.objects.filter(
        finished=False).filter(scientist=user)
    for pj in scientist_objects:
        pj_list.append(pj)

    context["data"] = pj_list
    context["Finalized"] = False

    return render(request, "webapp/privateprojects.html", context)

# Prpjetos arquivados Cientista


def MyArchivedProjectsS(request):
    """ View que demonstra os projetos arquivados do utilizador  """
    context = {}
    pj_list = []
    user = request.user.scientist
    scientist_objects = Project.objects.filter(
        finished=True).filter(scientist=user)
    for pj in scientist_objects:
        pj_list.append(pj)

    context["data"] = pj_list
    context["Finalized"] = True

    return render(request, "webapp/privateprojects.html", context)

# Download Apk


def download_apk(request):
    # Full path of file
    file_path = DOWNLOAD_DIR + '\cos.apk'
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/force_download")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404


def donator_exit_project(request, pk):
    """ Permite ao cientista finalizar o projeto """
    project = get_object_or_404(Project, pk=pk)
    userid = request.user.donator.id
    datag = DataGive.objects.filter(project=project).filter(donator=userid)
    datag.delete()
    return redirect("webapp:myDprojects")


def faq(request):
    return render(request, "webapp/faq.html")
