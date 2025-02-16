from django.contrib import admin
from Account import models

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'avatar')


admin.site.register(models.User, UserAdmin)
