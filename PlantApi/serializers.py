from rest_framework import serializers
from Core.models import Plant, DataTable, Sensor, NPKSensor


class PlantSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Plant
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Sensor
        fields = '__all__'

class NPKSensorSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = NPKSensor
        fields = '__all__'


class DataTableSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = DataTable
        fields = '__all__'
