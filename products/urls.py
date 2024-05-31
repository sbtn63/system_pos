from django.urls import path

from .views import ListProductsView, CreateProductView, DeleteProductAdminView, UpdateProductAdminView

urlpatterns = [
    path('', ListProductsView.as_view(), name='list_products'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('update/<int:pk>', UpdateProductAdminView.as_view(), name='update_product'),
    path('delete/<int:pk>', DeleteProductAdminView.as_view(), name='delete_product'),
]
