Virtual env é super importante, serve para testar as features de novos updates dos packages de por exemplo a linguagem
Tudo o que for instalado no env so vai ficar no env


Comandos:

# Django

## Project

**Ficheiros project:**
>
>__init.py__
>>
>>init.py file is a blanc python script that due to its special name let´s python know that this directory can be threated as a package
>
>__settings.py__
>>
>>Where we are going to savee allof our project settings.
>
>__urls.py__
>>
>>Is a pyfile script where we will store all the URL patterns for our porject. Basicly the different pages of our web application
>
>__wsgi.py__
>>
>>This is a python script that acts as the web server gateway interface
>__manage.py__
>>
>>This is a python script that associates with many commands as we build our app  

**RunServer**
>python manage.py runserver


**O que é uma migration?**
>uma migration permitenos mover um base de dados de um design para outro

**Django Project**
> É uma coleção de aplicações e configurações que quando combinadas fazem uma aplicacão web  completa.

**Django Aplication**
> É criado quando queremos performar uma funcionalidade particular da aplicacão (p.e, podemos ter a app de registro ou de comments etc)

## APP

**Ficheiros app:**
>
>__init.py__
>>
>>init.py file is a blanc python script that due to its special name let´s python know that this directory can be threated as a package
>
>__admin.py__
>>
>>Where we can register models which django will then use them with djangos admin interface
>
>__apps.py__
>>
>>Here we gone place application specific configurations
>
>__models.py__
>>
>>Store aplication data models
>__test.py__
>>
>>Here we can store functons to test our app
>
>__views.py__
>>
>>Here we have functions that handle requests and return responses
>
>__migrations folder__
>>
>>This directory stores database specific information as it relates to the models


**Funcionamento apos criar uma app**
>Temos de avisar o project que cruamos uma app, ou seja, ir aos settings.py file e adicionar ao INSTALLED_APPS.
>__Criar uma view__
>>abrir os views.py e criar uma função com a view.

>> e por ultimo adicionar a view aos urls do project.

**URL Mapping methods**
>vamos usar o include() importando do django.conf.urls

**Django Templates**
>Templates will contain the static parts of an html page(parts that are always the same)

> precisamos de adicioanr a pasta templates e ter uma pasta dentro desta com o nome da nossa app e adicioanr esta pasta templates as settings do project de modo a ser reconhecida como tal.

**Django Static Files**
>{%load static%}

>temos sempre de mencioanr de onde provem os static ou seja criar todas as diretorias necessarias para os importar

>templates vão ser ainda os sitios onde vamos guardas as umagens e os css necessarios.

>STATICFILES_DIRS = [
    STATIC_DIR,
]

**Django Models**
>Criar os models atranves do parametro models.models

>python manage.py migrate

>python manage.py makemigrations "nome da app"

>python manage.py migrate

>depois precisamos de registar os nossos models na admin pages
>criar um superuser!

>python manage.py createsuperuser

    form django.db import Models
    class user(models.model):
      top_name = models.CharField(max_lenght = 264, unique = true)


**Paradigma das views**
>MTV - Models, templates, views
>Way to show dynamic information!

>First: in the views.py file we import any models that we will need to use

>second: Use the view to query the model for data that we will need

>Third: Pass results form the model to the template

>Fourth: Edith the template so that it is ready to accept and display the data from the model.

>Fifth: Map a URL to the view

>Sith register de model in admin page, import models from app and write like this admin.site.register(modelname)


## User Input##

__Django Forms__

>Gerar html widges mais facilemnte com template tagging
>Our own validation rules

**Como lidar com as Django Forms?**

>Primeiro criar o ficheiro forms.py dentro da aplicação

    from django import Forms
    class FormName(forms.Form):
      name = forms.Charfield()
      email = forms.EmailField()
      text = forms.Charfield(widget = forms.Textarea)

>Agora que criamos a nossa form temos de a demonstrar usando a nossa view!

>Primeiro temos de importar a forms para o file view

>Depois temos de criar a view

      def form_view (request):
      form = forms.FormName()
      return render(request, "form_name.html", {"form":form})

> Depois ligar a view ao url file

>Depois podemos criar o template file, nao esqucer de dar uptade o settings file do templates

>Depois temos de entrar no template e injetar a form de tres maneiras
>> {{ form }}

----------------------------------
**HTTP**
>Metodos get e post

>get -requests data from a resource

>post submits data to be process to a resource

----------------------------------

 >{% csrf_token %} - is a security mesure, that secures HTTP POST, action that is initiated on the subsequent submission of a form

**Form Validation**
> add check for emptyfields

> check for a bot

>add a clean method for the entire form

>Exemple

        class FormName (forms.Form):
            name = forms.CharField()
            email = forms.EmailField()
            verify_email = forms.EmailField(label = "Enter your email again")
            text = forms.CharField(widget=forms.Textarea)
            botcatcher = forms.CharField(required=False,
                                        widget=forms.HiddenInput)


            def clean(self):
                all_clean_data = super().clean()
                email = all_clean_data["email"]
                vmail = all_clean_data["verify_email"]
                if email != vmail:
                    raise forms.ValidationError("Make s ure emails match!")

**Model Form**

>forms.py

        from django import forms
        from a2.models import User

        class userf(forms.ModelForm):
            class Meta():
                model = User
                fields = "__all__"

>views.py

        def initial(request):
            form = userf()

            if request.method == "POST":
                form = userf(request.POST)

                if form.is_valid():
                    form.save(commit = True)
                    return users(request)
                else:
                    print("Error Form invalid")


            return render(request, "p2/index.html", {"form":form})


**Url by anchor tags**

      <a href="basicapp/thankyou">Thanks</a>
can be changed to
      <a href="{% url "thanku" %}"></a>
or
      <a href="{% url "basicapp:thankyou" %}"> Thanks </a>

>nos url temos de dar o app_name= "basic_app"

>ja no template temos de adicionar na achor tag

      <a href="{% url "basic_app:other" %}">The other page</a>

>o other é consoante a view

**Template inheritance**

> DRY coding principles

>Template inheritance allows us to create a base template we can inherit from

>Inheritance allows us to use multiple base html files

>The main steps for inheritance

>>Find the repetitive parts of your Project

>>Create a base template of them

>>Set the tags in the base template

>>Extend and call those tags


**Features and Filters**





**Django Passwords**
We gone begin by using PBKDF2 with sha256 that is already built in django
we can use validators to make better passwords
input password and save the hash
we cant have two pieces of data with the same hash
we cant revert the hash
We first need to look at the settings!


**When we install something in settints installed app we should migrate allways**


**Logins**
This process involves:
>Setting up the login views

>Using built-in decorators for acess

>Adding the login_url in settings

>create login.html

>edit url.py files


**Deploy**


**CBV - Class Based Views**
First we need to import

>from django.views.generic import View, TemplateView

__as_view()__ grab that class and show as view


**CRUD**

Create, Retrieve, Update and Delete

**Tokens Command Verify!**

curl -v -d "username=ramosd1&password=asd" http://www.citizensonscience.xyz/webapp/api-token-auth/
