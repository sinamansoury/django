from django.urls import path

from Rent import views

urlpatterns = [
    path('', views.RentListView.as_view(), name='rent-view'),
    path('cat/<cat>', views.RentListView.as_view(), name='rent_category_list'),
    path('add-comment', views.add_rent_comment, name='add-comment'),
    path('<str:slug>', views.RentDetailView.as_view(), name='rent_detail'),
]
