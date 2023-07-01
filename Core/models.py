from django.db import models

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
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="photos/plants/%Y/%m/%d/")
    ec = models.CharField(max_length=1000)
    ph = models.CharField(max_length=1000)
    npk = models.CharField(max_length=1000)
    temperature = models.CharField(max_length=1000)
    ideal_moisture = models.CharField(max_length=1000)
    fertilizer = models.CharField(max_length=1000)




