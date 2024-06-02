from django.urls import path

from .views import ListSupplierView, CreateSupplierView, UpdateSupplierView, DeleteSupplierView

urlpatterns = [
    path('', ListSupplierView.as_view(), name='list_suppliers'),
    path('create/', CreateSupplierView.as_view(), name='create_supplier'),
    path('update/<int:pk>/', UpdateSupplierView.as_view(), name='update_supplier'),
    path('delete/<int:pk>/', DeleteSupplierView.as_view(), name='delete_supplier')
]
