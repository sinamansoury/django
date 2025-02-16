from django.urls import path
from User_panel import views

urlpatterns = [
    path('', views.UserPanelView.as_view(), name='User_panel'),
    path('edit-profile', views.EditUserInfo.as_view(), name='Edit-profile'),
    path('change-password', views.ChangePassword.as_view(), name='Change-password'),
    path('authenticated', views.Authenticated.as_view(), name='Authenticated'),
    path('user-basket', views.user_basket_panel, name='User-basket'),
    path('user-rent-basket', views.user_rent_basket_panel, name='User-rent-basket'),
    path('orders', views.UserOrder.as_view(), name='orders'),
    path('rent-orders', views.UserRentOrder.as_view(), name='rent-orders'),
    path('orders-detail/<order_id>', views.user_detail, name='orders-detail'),
    path('orders-rent-detail/<order_rent_id>', views.user_rent_detail, name='orders-rent-detail'),
    path('delete-product', views.remove_order_item, name='Delete-product'),
    path('change-product-number', views.change_product_number, name='Change-product-number'),
    path('delete-rent-product', views.remove_rent_order_item, name='Delete-rent-product'),
    path('change-rent-product-number', views.change_rent_product_number, name='Change-rent-product-number'),
]
