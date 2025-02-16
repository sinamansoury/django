from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactUsCreateView.as_view(), name='contact_us'),
    path('profile/', views.ContactUsUploadFileView.as_view(), name='ContactUsProfile'),
    path('profiles/', views.ProfileImagesCreateView.as_view(), name='ProfileImagesCreate')
]
