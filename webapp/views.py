from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from webapp.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .decorators import scientist_required, donator_required, owner_required
from webapp import models
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm




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
            email = user_form.cleaned_data.get("email")
            first_name = scientist_form.cleaned_data.get("first_name")
            last_name = scientist_form.cleaned_data.get("last_name")
            phone = scientist_form.cleaned_data.get("phone")
            address = scientist_form.cleaned_data.get("address")
            work_local = scientist_form.cleaned_data.get("work_local")
            bi = scientist_form.cleaned_data.get("bi")
            bis = Scientist.objects.order_by("bi")
            for u in bis:
                if bi == u.bi:return messages.error(request, 'This bi already exists!')
            if 10000000 < bi < 99999999 and 90000000 < phone < 999999999:
                scientist_profile = Scientist(
                    first_name=first_name, last_name=last_name, address=address, work_local=work_local, bi=bi, phone=phone, email=email)
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                scientist_profile.user = user
                scientist_profile.save()
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
            donator_profile =Donator(age=age, email=email)
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
            messages.error(request, 'username or password not correct')
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
                return HttpResponse("<h1>Project Created!!</h1>")
        else:
            print(project_form.errors)
    else:
        project_form = ProjectForm
    return render(request, "webapp/project_form.html", {"form": project_form})


@method_decorator([login_required, scientist_required], name='dispatch')
class ProjectListView(ListView):
    context_object_name = "projects"
    model = models.Project

    


@method_decorator([login_required], name='dispatch')
class ProjectDetailView(DetailView):
    context_object_name = "project"
    model = models.Project
    template_name = "webapp/project_detail.html"


@method_decorator([login_required, scientist_required, owner_required], name='dispatch')
class ProjectUpdateView(UpdateView):
    model = models.Project
    fields = ("name", "description",)
    success_url = reverse_lazy('webapp:list')


@method_decorator([login_required, scientist_required, owner_required], name='dispatch')
class ProjectDeleteView(DeleteView):
    model = models.Project
    success_url = reverse_lazy("webapp:list")


def DataGiveView(request, pk):
    """ Cria o objeto DataGive, ou seja, a partir da criação deste objeto o donator faz parte do projeto"""

    if DataGive.objects.filter(project=pk).filter(donator=request.user.donator.id).exists():
        """ Serve para verificar se o donator ja faz parte do projeto e se sim ir para a detailview do mesmo """

        pks = str(pk)
        return HttpResponseRedirect("mydonatorprojects/"+ pks)

    in_project = False
    if request.method == "POST":
        """ Criação do objeto DataGive """
        project = get_object_or_404(Project, pk=pk)
        donator = request.user.donator
        datagive = DataGive(project=project, donator=donator)
        datagive.save()
        in_project = True
    return render(request, "webapp/project_registry.html", {"in_project": in_project})


def DonatorList(request):
    """ Lista de todos os projetos do donator """

    pd_list = Project.objects.order_by("name")

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


@login_required
@scientist_required
def privateScientistProjectView(request):
    """ Vista dos proprios projetos dos cientistas """
    context = {}
    user_id = request.user.scientist.id
    projects_list = Project.objects.filter(owner=user_id)
    context["data"] = projects_list
    return render(request, "webapp/privateprojects.html", context)


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
    print(context)

    return render(request, "webapp/privateprojects.html", context)









