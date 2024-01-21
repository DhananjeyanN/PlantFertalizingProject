from django.contrib.auth.models import User
from django.db import models

from accounts.models import Profile


# Create your models here.


# class Temperature(models.Model):
#     level = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.level
#
#
# class Moisture(models.Model):
#     level = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.level
#
#
# class EC(models.Model):
#     level = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.level
#
#
# class Fertilizer(models.Model):
#     level = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.level
#
#
# class PH(models.Model):
#     level = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.level
#
#
# class NPK(models.Model):
#     level = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.level
#

class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plant_user')
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="photos/plants/%Y/%m/%d/", blank=True, null=True)
    ec = models.CharField(max_length=1000)
    ph = models.CharField(max_length=1000)
    nitrogen = models.CharField(max_length=1000)
    phosphorus = models.CharField(max_length=1000)
    potassium = models.CharField(max_length=1000)
    temperature = models.CharField(max_length=1000)
    ideal_moisture = models.CharField(max_length=1000)
    fertilizer = models.CharField(max_length=1000)
    plant_coefficient = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class DataTable(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='data')
    uuid = models.CharField(max_length=200, primary_key=True)
    m_temp = models.FloatField(null=True, blank=True)
    m_moist = models.FloatField(null=True, blank=True)
    m_ec = models.FloatField(null=True, blank=True)
    m_nitrogen = models.FloatField(null=True, blank=True)
    m_phosphorus = models.FloatField(null=True, blank=True)
    m_potassium = models.FloatField(null=True, blank=True)
    m_ph = models.FloatField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    # {'plant_id': 14, 'uuid': '704f03eb-64d1-41cc-b2fa-96fd981149d4', 'm_temp': 'None',
    # 'm_moist': '33.000000', 'm_ec': 'None', 'm_nitrogen': 'None', 'm_phosphorus': 'None',
    # 'm_potassium': 'None', 'm_ph': 'None', 'date_time': '2023-10-31 21:29:29'}

    def __str__(self):
        return f'data recorded at Date {self.date_time} EC {self.m_ec} Nitrogen {self.m_nitrogen} Phosphorus {self.m_phosphorus} Potassium {self.m_potassium} PH {self.m_ph} MOIST {self.m_moist}'


class Sensor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sensor_user')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='sensor')
    sensor_pin = models.IntegerField()
    sensor_type = models.IntegerField()

    def __str__(self):
        return f'Plant: {self.plant} Pin: {self.sensor_pin} Type: {self.sensor_type}'


class NPKSensor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='npk_user')
    sensor_pin = models.IntegerField()
    current_plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='npk_sensor')

    def __str__(self):
        return f'Current Plant: {self.current_plant} Pin: {self.sensor_pin}'
