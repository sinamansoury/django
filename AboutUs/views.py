from django.shortcuts import render
from django.views.generic import TemplateView

from Site_settings.models import SiteSettings
from tracking.mixins import LoggingMixins


# Create your views here.


class AboutUsView(LoggingMixins, TemplateView):
    template_name = 'AboutUs/About_Us_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_us_setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
        context['about_us_setting'] = about_us_setting

        return context
