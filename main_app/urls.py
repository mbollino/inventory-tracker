from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.product_index, name='product_index'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('products/create/', views.ProductCreate.as_view(), name='product_create'), 
    path('products/<int:pk>/update/', views.ProductUpdate.as_view(), name='product_update'), 
    path('products/<int:pk>/delete/', views.ProductDelete.as_view(), name='product_delete'), 
    path('products/<int:product_id>/add-order/', views.add_order, name='add_order'),
    path('suppliers/create/', views.SupplierCreate.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/', views.SupplierDetail.as_view(), name='supplier_detail'),
    path('suppliers/', views.SupplierList.as_view(), name='supplier_index'),
     
]