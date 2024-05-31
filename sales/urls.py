from django.urls import path

from .views import SaleListView, CreateSaleView, DeleteSaleView

urlpatterns = [
    path('', SaleListView.as_view(), name='sale_list'),
    path('create/', CreateSaleView.as_view(), name='sale_create'),
    path('delete/<int:pk>', DeleteSaleView.as_view(), name='sale_delete')
]
