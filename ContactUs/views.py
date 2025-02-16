from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, CreateView, ListView

from Site_settings.models import SiteSettings
from tracking.mixins import LoggingMixins
from .forms import ContactUsModelForm
from .models import ContactUs, ProfileImages


# Create your views here.
class ContactUsCreateView(LoggingMixins, CreateView):
    form_class = ContactUsModelForm
    template_name = 'shared/contact_us_page.html'
    success_url = '/contact-us/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_us_setting: SiteSettings = SiteSettings.objects.filter(is_main_settings=True).first()
        context['about_us_setting'] = about_us_setting

        return context


class ContactUsUploadFileView(CreateView):
    template_name = 'shared/profile.html'
    model = ProfileImages
    fields = '__all__'
    success_url = '/contact-us/profile/'


class ProfileImagesCreateView(ListView):
    model = ProfileImages
    template_name = 'shared/profile_page.html'
    context_object_name = 'profiles'


