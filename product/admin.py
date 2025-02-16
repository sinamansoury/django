from django.contrib import admin

from product import models


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active']
    list_filter = ['is_active', 'category']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrands)
admin.site.register(models.ProductVisit)
admin.site.register(models.Size)
admin.site.register(models.Gallery)
admin.site.register(models.ProductComment)
