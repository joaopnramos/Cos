from rest_framework import serializers
from .models import DataGive, Data, Project


class DataSerializer(serializers.ModelSerializer):
    """ Serializa a Data, ou seja, transforma em gson e disponibiliza """

    class Meta:
        model = Data
        fields = "__all__"
        
    
class ProjectSerializer(serializers.ModelSerializer):
    """ Serializa o Projeto, ou seja, transforma em gson e disponibiliza """
    class Meta:
        model = Project
        fields = "__all__"
      
class DataGiveSerializer(serializers.ModelSerializer):
    """ Serializa o DataGive, ou seja, transforma em gson e disponibiliza """

    class Meta:
        model = DataGive
        fields = "__all__"
        



