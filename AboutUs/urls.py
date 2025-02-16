from django.urls import path
from AboutUs import views

urlpatterns = [
    path('about-us', views.AboutUsView.as_view(), name='About_Us')
]
