from django.contrib import admin
from Home_module import models


# Register your models here.


class SlidersAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active')


admin.site.register(models.Sliders, SlidersAdmin)
