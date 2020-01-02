# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime

# Create your models here.

class Sorteo(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(default=datetime.now)
    nombre = models.CharField(max_length=100)
    hashtag = models.CharField(max_length=500)
    ganador = models.CharField(max_length=100, default='')

    def guardar(self):
        self.save()

    def __unicode__(self):
        return self.id

class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    texto = models.CharField(max_length=500)
    sorteo = models.ForeignKey('Sorteo',on_delete=models.CASCADE)

    def guardar(self):
        self.save()

    def __unicode__(self):
        return self.id