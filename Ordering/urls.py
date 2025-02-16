from django.urls import path
from . import views

urlpatterns = [
    path('add-to-order', views.add_to_order, name='add_to_order'),
    path('add-to-rent-order', views.add_to_rent_order, name='add_to_rent_order'),
    path('payment/', views.send_order_payment, name='payment'),
    path('verify-payment/', views.verify_payment, name='verify'),
]
