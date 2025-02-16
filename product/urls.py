from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_category_list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product_brand'),
    path('product-favorite', views.ProductAddFavoriteView.as_view(), name='product-favorite'),
    path('add-comment', views.add_product_comment, name='add-comment'),
    path('<str:slug>', views.ProductDetailView.as_view(), name='product_detail'),

]
