from django.urls import path

from .views import ListStockReceptionView, CreateStockReceptionView, DeleteStockReceptionView

urlpatterns = [
    path('', ListStockReceptionView.as_view(), name='list_stock_receptions'),
    path('create/', CreateStockReceptionView.as_view(), name='create_stock_reception'),
    path('delete/<int:pk>/', DeleteStockReceptionView.as_view(), name='delete_stock_reception')
]
