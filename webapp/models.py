from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField
from webapp.choices import PERIOD_CHOICES ,SPACE_TIME_CHOICES, SENSORS_CHOICES

#Token addition to user profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
# Create your models here.



#Cientista!
class Scientist(models.Model):
    user = models.OneToOneField(User, related_name='scientist', on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, null=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work_local = models.CharField(max_length=100)
    bi = models.PositiveIntegerField(unique=True)
    address = models.CharField(max_length=100, blank=True)
    is_scientist = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(null = True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


#Doador de dados
class Donator(models.Model):
    age = models.IntegerField()
    email = models.EmailField(max_length=254, null=False, unique=True)
    user = models.OneToOneField(User, related_name='donator', on_delete=models.CASCADE)
    is_donator = models.BooleanField(default=True)
    

#Projetos dos cientistas
class Project(models.Model):
    """ Objeto Projeto, criado apenas pelo cientista e ofere todos as
        caracteristicas desejasdas pelo cientista """
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.IntegerField()
    scientist = models.ForeignKey(Scientist, on_delete=models.CASCADE, related_name="scientist")
    donator = models.ManyToManyField(Donator, blank=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    periodChoice = models.CharField(max_length=2, choices=PERIOD_CHOICES)
    spacetimeChoice = models.CharField(max_length=2, choices=SPACE_TIME_CHOICES)
    sensorsChoice = MultiSelectField(choices=SENSORS_CHOICES)
    finished = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse("webapp:detail", kwargs={"pk": self.pk})

    def project_finished(self):
        """ Da um projeto como terminado """
        self.finished = True
        return self.finished

    def __str__(self):
        return self.name


#Scensors Data!
class Data(models.Model):
    """ A partir deste objeto é possiver fornecer os dados recolhidos a cada projeto """

    owner = models.ForeignKey(Donator, on_delete=models.CASCADE, related_name="data")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="data")
    alls = models.CharField( max_length=50)
    camera = models.CharField( max_length=50)
    light = models.CharField( max_length=50)
    ground = models.CharField( max_length=50)
    
    def __str__(self):
        return "informação deste projeto" + self.alls

#Model que permite ligar o donator aos projects
class DataGive(models.Model):
    """ Serve para criar um objeto que liga os projetos e os donators,
        a partir deste objeto os donators têm a possibilidade de se juntarem
        a um projeto. """
    donator = models.ForeignKey(Donator, on_delete=models.CASCADE, related_name="give_data")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="give_data")
    givingFinished = models.BooleanField(default=False)

    def projectDone(self):
        """ Esta variavel boleana permite á query no telemovel saber se 
            este projeto ainda é passivel de requisição de dados """
        self.givingFinished = True
        return self.givingFinished

    
    