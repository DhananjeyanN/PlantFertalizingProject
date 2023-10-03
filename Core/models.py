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
    npk = models.CharField(max_length=1000)
    temperature = models.CharField(max_length=1000)
    ideal_moisture = models.CharField(max_length=1000)
    fertilizer = models.CharField(max_length=1000)
    plant_coefficient = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class DataTable(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='data')
    uuid = models.CharField(max_length=200, null=True, blank=True)
    m_temp = models.FloatField(null=True, blank=True)
    m_moist = models.FloatField(null=True, blank=True)
    m_ec = models.FloatField(null=True, blank=True)
    m_npk = models.FloatField(null=True, blank=True)
    m_ph = models.FloatField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'data recorded at Date {self.date_time} EC {self.m_ec} NPK {self.m_npk} PH {self.m_ph} MOIST {self.m_moist}'





