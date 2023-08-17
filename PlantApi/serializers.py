from rest_framework import serializers
from Core.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Plant
        fields = '__all__'
