from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator
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
    phone = models.PositiveIntegerField(unique=True)
    image = models.ImageField()
    email = models.EmailField(max_length=254, null=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work_local = models.CharField(max_length=100)
    bi = models.PositiveIntegerField(unique=True)
    address = models.CharField(max_length=100, blank=True)
    is_scientist = models.BooleanField(default=True)
    
 
    

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
    owner = models.IntegerField()
    scientist = models.ForeignKey(Scientist, on_delete=models.CASCADE, related_name="scientist")
    donator = models.ManyToManyField(Donator, blank=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    periodChoice = models.CharField(max_length=2, choices=PERIOD_CHOICES)
    spacetimeChoice = models.CharField(max_length=2, choices=SPACE_TIME_CHOICES)
    sensorsChoice = models.CharField(max_length=2, choices=SENSORS_CHOICES)
    finished = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse("webapp:detail", kwargs={"pk": self.pk})
    
    def project_finished(self):
        self.finished = True
        return self.finished

    def __str__(self):
        return self.name


#Scensors Data!
class Data(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="data")
    data = models.FileField(upload_to='uploads/')
    def __str__(self):
        return "informação deste projeto" + self.data

#Model que permite ligar o donator aos projects
class DataGive(models.Model):
    donator = models.ForeignKey(Donator, on_delete=models.CASCADE, related_name="give_data")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="give_data")
    projectFinished = models.BooleanField(default=False)

    def projectDone(self):
        self.projectFinished = True
        return self.projectFinished
        
    