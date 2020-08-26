from rest_framework import serializers
from .models import DataGive, Data, Project


class DataSerializer(serializers.ModelSerializer):
    """ Serializes a user profile project """

    class Meta:
        model = Data
        fields = "__all__"
        
    
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
      
class DataGiveSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = DataGive
        fields = "__all__"
        



