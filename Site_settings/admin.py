from django.contrib import admin
from . import models
# Register your models here.


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'links')


class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'position')


admin.site.register(models.SiteSettings)
admin.site.register(models.FooterLinkBox)
admin.site.register(models.FooterLink, SiteSettingsAdmin)
admin.site.register(models.BannerSite, SiteBannerAdmin)
