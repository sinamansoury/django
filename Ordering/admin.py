from django.contrib import admin
from . import models
from .models import OrderingItem, Ordering
# Register your models here.

admin.site.register(models.Ordering)
admin.site.register(models.OrderingItem)
