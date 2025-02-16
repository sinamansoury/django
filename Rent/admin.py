from django.contrib import admin

from Rent import models

# Register your models here.
class RentAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active']
    list_filter = ['is_active', 'category']


admin.site.register(models.Rent, RentAdmin)
admin.site.register(models.RentCategory)
admin.site.register(models.RentVisit)
admin.site.register(models.RentSize)
admin.site.register(models.Gallery)
admin.site.register(models.RentComment)
admin.site.register(models.RentDay)
