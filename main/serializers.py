from rest_framework import serializers
from .models import *


class AndroidDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AndroidData
        fields = "__all__"


class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = "__all__"
