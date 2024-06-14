from django.urls import path

from .views import ListSupplierView, CreateSupplierView, UpdateSupplierView, DeleteSupplierView

urlpatterns = [
    path('', ListSupplierView.as_view(), name='list'),
    path('create/', CreateSupplierView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateSupplierView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteSupplierView.as_view(), name='delete')
]
