from django.contrib import admin
from .models import Scientist, Donator, Project, Data, DataGive

# Register your models here.
admin.site.register(Scientist)
admin.site.register(Donator)
admin.site.register(Project)
admin.site.register(Data)
admin.site.register(DataGive)