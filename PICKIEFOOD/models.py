from django.db import models

# Create your models here.


class Infos(models.Model):
    name = models.CharField(max_length=200)
    dob = models.CharField(max_length=200)
    nation = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    religon = models.CharField(max_length=200)
    dietary = models.CharField(max_length=200)
    height = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    illness = models.CharField(max_length=200)
    allergen = models.CharField(max_length=200)