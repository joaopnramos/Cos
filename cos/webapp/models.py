from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.



#Cientista!
class Scientist(models.Model):
    user = models.OneToOneField(User, related_name='scientist', on_delete=models.CASCADE)
    phone = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work_local = models.CharField(max_length=100)
    bi = models.IntegerField()
    address = models.CharField(max_length=100, blank=True)
    is_scientist = models.BooleanField(default=True)
 
    

    def __str__(self):
        return self.first_name + " " + self.last_name

#Doador de dados

   

#Projetos dos cientistas
class Project(models.Model):
    scientist = models.ForeignKey(Scientist, on_delete=models.CASCADE, related_name="scientist")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def get_absolute_url(self):
        return reverse("webapp:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

class Donator(models.Model):
    age = models.IntegerField()
    user = models.OneToOneField(User, related_name='donator', on_delete=models.CASCADE)
    is_donator = models.BooleanField(default=True)
    projects = models.ManyToManyField(Project, through="DataGive")
    
class Primitivas(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="primitivas")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Data(models.Model):
    project = models.OneToOneField(Project, related_name=("data"), on_delete=models.CASCADE)
    data = models.FileField(upload_to='uploads/')
    def __str__(self):
        return "informação deste projeto" + self.project.name


class DataGive(models.Model):
    donator = models.ForeignKey(Donator, on_delete=models.CASCADE, related_name="give_data")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="give_data")