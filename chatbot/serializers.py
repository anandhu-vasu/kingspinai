from rest_framework import serializers
from .models import *

class detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserData
        fields='__all__'

