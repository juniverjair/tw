from django.contrib import admin

# Register your models here.
from .models import Sorteo, Tweet

admin.site.register(Sorteo)
admin.site.register(Tweet)