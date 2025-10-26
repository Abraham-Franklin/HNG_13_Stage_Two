from rest_framework import serializers
from .models import CountryData

class CountryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryData
        fields = "__all__"
