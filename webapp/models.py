from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.


# Cientista!
class Scientist(models.Model):
    user = models.OneToOneField(User, related_name='scientist', on_delete=models.CASCADE, blank=False)
    phone = models.IntegerField()
    image = models.ImageField()
    email = models.EmailField(max_length=254, null=True)
    first_name = models.CharField(max_length=254, blank=False)
    last_name = models.CharField(max_length=254, blank=False)
    work_local = models.CharField(max_length=254, blank=False)
    bi = models.IntegerField()
    address = models.CharField(max_length=254, blank=True)
    is_scientist = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

# Doador de dados
class Donator(models.Model):
    age = models.IntegerField()
    email = models.EmailField(max_length=254, null=True)
    user = models.OneToOneField(User, related_name='donator', on_delete=models.CASCADE)
    is_donator = models.BooleanField(default=True)


# Projetos dos cientistas
class Project(models.Model):
    scientist = models.ForeignKey(Scientist, on_delete=models.CASCADE, related_name="scientist")
    donator = models.ManyToManyField(Donator, )
    name = models.CharField(max_length=254)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Primitivas(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="primitivas")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Data(models.Model):
    project = models.OneToOneField(Project, related_name="data", on_delete=models.CASCADE)
    data = models.FileField(upload_to='uploads/')

    def __str__(self):
        return "informação deste projeto" + self.project.name
