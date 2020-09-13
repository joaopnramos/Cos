from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from .decorators import scientist_required, donator_required, owner_required
from webapp import models
from .serializers import DataSerializer, ProjectSerializer, DataGiveSerializer, DonatorSerializer
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
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from cos.settings import DOWNLOAD_DIR, STATIC_DIR
import os
import csv
import re

#Index, pagina inicial
def indexView(request):
    """ pagina inicial, com form para enviar sugestões """
    context = {}
    if request.method == "POST":
        sue_form = SendUsEmail(data=request.POST)
        if sue_form.is_valid():
            name = sue_form.cleaned_data.get("name")
            message = sue_form.cleaned_data.get("message")
            emails = "citizensonscienceproject@gmail.com"
            email_subject = "Suggestion by " + name
            email_body = "User " + name + " has a suggestion." + "The message is: \n" + message + "."
            email = EmailMessage(
                    email_subject, email_body, "noreply@semycolon.com", [emails],)
            email.send(fail_silently=False)

    context["send_us_email"] = SendUsEmail
    return render(request, "webapp/index.html", context)


#Register View
class RegisterView(TemplateView):
    """ Pagina de escolha do tipo de utilizador que se
        pretende registrar """

    template_name = "webapp/generic_register.html"

# Registro do Cientista!!
def scientist_register(request):
    """ View destinada ao registo do cientista """

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        scientist_form = ScientistForm(data=request.POST)
        if user_form.is_valid() and scientist_form.is_valid():
            emails = user_form.cleaned_data.get("email")
            first_name = scientist_form.cleaned_data.get("first_name")
            last_name = scientist_form.cleaned_data.get("last_name")
            address = scientist_form.cleaned_data.get("address")
            work_local = scientist_form.cleaned_data.get("work_local")
            bi = scientist_form.cleaned_data.get("bi")
            bis = Scientist.objects.order_by("bi")

            for u in bis:
                if bi == u.bi:
                    messages.error(request, 'This BI already exists. Use another BI.')

            if 10000000 < bi < 99999999:
                scientist_profile = Scientist(first_name=first_name, last_name=last_name, address=address, work_local=work_local, bi=bi, email=emails)
                if scientist_form.cleaned_data.get("profile_pic"):
                    scientist_profile.profile_pic = scientist_form.cleaned_data.get("profile_pic")
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
                email_body = "Hi " + first_name + " " + last_name + "! \n" \
                    "Please use this link to verify the account:\n" + activate_url \
                    + "\nIf this isn't you, ignore this email." + "\n\nFrom the CoS Team."
                email = EmailMessage(
                    email_subject, email_body, "noreply@semycolon.com", [emails],)
                email.send(fail_silently=False)

                registered = True

            else:
                messages.error(request, 'Phone number or CC is wrong.')

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
            user.is_active = False
            user.save()
            donator_profile.user = user
            donator_profile.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse("activate", kwargs={
                            "uidb64": uidb64, "token": tokengenerator.make_token(user)})
            email_subject = "Activate you accounts"
            activate_url = "http://" + domain+link
            email_body = "Hi " + user.username + "! \n" \
                "Please use this link to verify the account:\n" + activate_url \
                + "\nIf this isn't you, ignore this email." + "\n\nFrom the CoS Team."
            email = EmailMessage(
                email_subject, email_body, "noreply@semycolon.com", [email],)
            email.send(fail_silently=False)
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
            messages.error(request, 'Username or Password is Incorrect.')
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
                name = request.POST.get("name")
                if Project.objects.filter(name=name).exists():
                    messages.error(request, "There is already a project with this name")
                    return redirect('webapp:project_create')
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

# Demonstra uma lista de todos os projetos aos cientistas
@method_decorator([login_required, scientist_required], name='dispatch')
class ProjectListView(ListView):
    """ Esta vista serve para ver todos os projeto """
    context_object_name = "projects"
    model = models.Project
    ordering = ['finished']

# Serve para demonstrar os detalhes de um projeto
@method_decorator([login_required], name='dispatch')
class ProjectDetailView(DetailView):
    """ Esta view serve para ver os detalhes do projeto """
    context_object_name = "project"
    model = models.Project
    template_name = "webapp/project_detail.html"

    """ Serve para dar contexto a detai view
        Neste caso vamos adicionar a informação de:
        *Quantos donators o projeto ofere
        *Quando foi o utlimo donate
        *Quando foi criado"""

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        """ numero de donators """
        number_donators = DataGive.objects.filter(
            project=self.kwargs.get('pk')).count()
        """ numero de donates """
        number_of_data = Data.objects.filter(
            project=self.kwargs.get('pk')).count()

        """ quando o projeto foi criado """
        created_date = Project.objects.get(id=self.kwargs.get('pk'))

        context['number_of_donators'] = number_donators
        context['number_of_data'] = number_of_data
        context['created_date'] = created_date.created_at

        return context

# Serve para atulizar um projeto e só está disponivel para os cientistas e para os donos no projeto
@method_decorator([login_required, scientist_required, owner_required], name='dispatch')
class ProjectUpdateView(UpdateView):
    """ Esta view serve para atualizar o projeto """
    model = models.Project
    fields = ("name", "description", "sensorsChoice",
              "periodChoice", "spacetimeChoice")
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

    pro = Project.objects.filter(id=pk)
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
    list_of_not = []
    dt = DataGive.objects.filter(donator=request.user.donator.id)
    for i in dt:
        list_of_not.append(i.project.id)
    pd_list = Project.objects.filter(finished=False).order_by("name").exclude(id__in=list_of_not)
    return render(request, "webapp/project_donator_list.html", context={"pd_list": pd_list})

# Profile
@login_required
@scientist_required
def profileScientist(request):
    """ Perfil do cientista """
    user = request.user
    if request.method == 'POST':
        u_form = UserUpdateForm(data=request.POST)
        s_form = ScientistUpdate(data=request.POST)

        if u_form.is_valid() and s_form.is_valid():
            users = request.user.scientist

            emails = user.email
            first_name = users.first_name
            last_name = users.last_name
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            if request.POST.get("first_name"):
                users.first_name = request.POST['first_name']
                users.save()

            if request.POST.get("work_local"):
                users.work_local = request.POST['work_local']
                users.save()

            if "profile_pic" in request.FILES:
                users.profile_pic = request.FILES['profile_pic']
                users.save()

            if request.POST.get("bi"):
                bi = s_form.cleaned_data.get("bi")
                bis = Scientist.objects.order_by("bi")
                for u in bis:
                    if bi == u.bi:
                        messages.error(request, 'This BI is already in use.')
                        return redirect('/webapp/profile/')
                users.bi = request.POST['bi']
                users.save()

            if request.POST.get("last_name"):
                users.last_name = request.POST['last_name']
                users.save()

            if request.POST.get("address"):
                users.address = request.POST['address']
                users.save()

            if request.POST.get("email"):
                user.email = request.POST["email"]
                user.save()

            if request.POST.get("password"):
                password = request.POST["password"]
                MIN_LENGTH = 8
                """Serve para verificar se o comprimento da password é o indicado """
                if len(password) < MIN_LENGTH:
                    messages.error(request, "The new password must be at least 8 characters long")
                    return redirect('/webapp/profile/')

                """Serve para verificar se existe pelo menos uma letra e caracter não letra """
                first_isalpha = password[0].isalpha()
                if all(c.isalpha() == first_isalpha for c in password):
                    messages.error(request, 'The new password must contain at least one letter and at least one digit or punctuation character')
                    return redirect('/webapp/profile/')
                user.is_active = False
                domain = get_current_site(request).domain
                link = reverse("activate", kwargs={
                               "uidb64": uidb64, "token": tokengenerator.make_token(user)})
                email_subject = "Activate you accounts"
                activate_url = "http://" + domain+link
                email_body = "Hi " + first_name + " " + last_name + "! \n" \
                    "Please use this link to verify the password change:\n" + activate_url \
                    + "\nIf this isn't you, ignore this email." + "\n\nFrom the CoS Team."
                email = EmailMessage(
                    email_subject, email_body, "noreply@semycolon.com", [emails],)
                email.send(fail_silently=False)
                user.set_password(password)  # replace with your real password
                user.save()

                return redirect("webapp:p_changed")

            messages.success(request, f'Your account has been updated!')
            return redirect('/webapp/profile/')
    else:
        u_form = UserUpdateForm()
        s_form = ScientistUpdate()

    context = {'u_form': u_form, "s_form": s_form}
    return render(request, 'webapp/profile.html', context)

#Template para alertar a alteração da parlvra pass
class PasswordChangedView(TemplateView):
    """ Pagina inicial do projeto """

    template_name = "webapp/password_change.html"

# Projetos dos proprios cientistas


@login_required
@scientist_required
def privateScientistProjectView(request):
    """ Vista dos proprios projetos dos cientistas """
    context = {}
    user_id = request.user.scientist.id
    projects_list = Project.objects.filter(owner=user_id)
    context["data"] = projects_list
    return render(request, "webapp/statusprojects.html", context)

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

    return render(request, "webapp/statusprojects.html", context)

# Serve para os cientistas finalizarem os projetos


@login_required
@scientist_required
def finishthedproject(request, pk):
    """ Permite ao cientista finalizar o projeto """
    project = get_object_or_404(Project, pk=pk)
    project.project_finished()
    project.save()
    dtobjs = DataGive.objects.filter(project=pk)
    for i in dtobjs:
        i.delete()
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
    search_fields = ("donator__id",)

class DonatorViewSet(ModelViewSet):
    """ Permite adicionar dados aos projetos através de gson, basicamente é um end point """

    serializer_class = DonatorSerializer
    queryset = Donator.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['user__id']

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
            messages.success(request, "Account activated sucessfully.")

        except Exception as ex:
            pass
        return redirect("user_login")

# Projetos ativos cientista
@login_required
@donator_required
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

    return render(request, "webapp/statusprojects.html", context)

# Projetos arquivados Donator

@login_required
@donator_required
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
    return render(request, "webapp/statusprojects.html", context)

# Projetos ativos Cientista

@login_required
@scientist_required
def MyActiveProjectsS(request):
    """ View que demonstra os projetos ativos do utilizador  """
    context = {}
    pj_list = []

    user = request.user.scientist
    scientist_objects = Project.objects.filter(
        finished=False)
    for pj in scientist_objects:
        pj_list.append(pj)

    context["data"] = pj_list
    context["Finalized"] = False

    return render(request, "webapp/statusprojects.html", context)

# Prpjetos arquivados Cientista

@login_required
@scientist_required
def MyArchivedProjectsS(request):
    """ View que demonstra os projetos arquivados do utilizador  """
    context = {}
    pj_list = []
    user = request.user.scientist
    scientist_objects = Project.objects.filter(
        finished=True)
    for pj in scientist_objects:
        pj_list.append(pj)

    context["data"] = pj_list
    context["Finalized"] = True

    return render(request, "webapp/statusprojects.html", context)

# Download Apk


def download_apk(request):
    # Full path of file
    file_path = STATIC_DIR + '\cos.apk'
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/force_download")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404

@login_required
@donator_required
def donator_exit_project(request, pk):
    """ Permite ao cientista finalizar o projeto """
    project = get_object_or_404(Project, pk=pk)
    userid = request.user.donator.id
    datag = DataGive.objects.filter(project=project).filter(donator=userid)
    datag.delete()
    return redirect("webapp:myDprojects")


def faq(request):
    return render(request, "webapp/faq.html")

@login_required
@scientist_required
def export_data(request, pk):
    """ Serve para traduzir as choices """
    sensors_dict = {"t": "temperature", "c": "proximity", "l": "light", "p": "pressure"}
    """ Recolhe os sensores requesitados pelo cientistas """
    sensors_requested = []
    temperature_data = []
    proximity_data = []
    light_data = []
    pressure_data = []
    data_export = []
    length = 0

    """ Função para recolher os sensores do projeto """
    pj = Project.objects.get(pk=pk)

    for i in pj.sensorsChoice:
        a = sensors_dict[i]
        sensors_requested.append(a)

    for sensor in sensors_requested:
        """ Organizado por utilizador de forma a poder ser recolhida a informação de uma forma mais simples """
        for data in Data.objects.filter(project=pk).order_by("owner").values_list(sensor):
            if sensor == "temperature":
                a = re.sub('[()]', '', data[0])
                temperature_data.append(a)

            elif sensor == "proximity":
                a = re.sub('[()]', '', data[0])
                proximity_data.append(a)

            elif sensor == "light":
                a = re.sub('[()]', '', data[0])
                light_data.append(a)

            elif sensor == "pressure":
                a = re.sub('[()]', '', data[0])
                pressure_data.append(a)

    if len(temperature_data) != 0:
        length = len(temperature_data)
    else:
        if len(proximity_data) != 0:
            length = len(proximity_data)
        else:
            if len(light_data) != 0:
                length = len(light_data)

            else:
                length = len(pressure_data)

    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    response['Content-Disposition'] = 'attachment; filename="{}_data.csv"'.format(
        pj.name)
    writer.writerow(sensors_requested)

    a = 0
    leng = length
    for i in range(leng):
        if int(pj.periodChoice) == a:
            writer.writerow(
                ["**************************Another user***********************"])
            a = 0
        a = a + 1
        data_export = []
        if temperature_data:
            data_export.append(temperature_data[i])

        if proximity_data:
            data_export.append(proximity_data[i])

        if light_data:
            data_export.append(light_data[i])

        if pressure_data:
            data_export.append(pressure_data[i])

        writer.writerow(data_export)
        i = i+1

    return response


@login_required
def see_scientist_profile(request, pk):

    """ Serve para os donators verem o perfil dos cientistas """
    scientist = Scientist.objects.get(id=pk)
    u = User.objects.get(id=scientist.user.id)
    context = {}
    context["uscientist"] = u
    context["scientist"] = scientist

    return render(request, "webapp/scientist_profile.html", context)

@login_required
@scientist_required
def FinalizingView(request, pk):
    """ Finalizar um projeto e enviar um email a todos os donators"""
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        """ Finalizado """
        sue_form = SendEmailForm(data=request.POST)
        if sue_form.is_valid():
            message = sue_form.cleaned_data.get("message")
            email_subject = "Finished of project " + project.name
            donators = DataGive.objects.filter(project= pk)
            email_list = []
            for i in donators:
                email = i.donator.email
                email_list.append(email)

            email_body = "Hi this is a message from the owner scientist of the project " + project.name + "\n" + message
            email = EmailMessage(
                    email_subject, email_body, "noreply@semycolon.com", email_list,)
            email.send(fail_silently=False)
            pks = str(pk)

            return HttpResponseRedirect("finish/" + pks )

    context = {}
    context["send_us_email"] = SendEmailForm
    context["project_name"] = project.name
    context["project_id"] = project.id
    return render(request, "webapp/project_finishing.html", context)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})