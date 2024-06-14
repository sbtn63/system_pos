from django.urls import path

from .views import ListProductsView, CreateProductView, DeleteProductAdminView, UpdateProductAdminView

urlpatterns = [
    path('', ListProductsView.as_view(), name='list'),
    path('create/', CreateProductView.as_view(), name='create'),
    path('update/<int:pk>', UpdateProductAdminView.as_view(), name='update'),
    path('delete/<int:pk>', DeleteProductAdminView.as_view(), name='delete'),
]
