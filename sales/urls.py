from django.urls import path

from .views import SaleListView, CreateSaleView, DeleteSaleView

urlpatterns = [
    path('', SaleListView.as_view(), name='list'),
    path('create/', CreateSaleView.as_view(), name='create'),
    path('delete/<int:pk>', DeleteSaleView.as_view(), name='delete')
]
