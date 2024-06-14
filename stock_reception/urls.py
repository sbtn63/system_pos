from django.urls import path

from .views import ListStockReceptionView, CreateStockReceptionView, DeleteStockReceptionView

urlpatterns = [
    path('', ListStockReceptionView.as_view(), name='list'),
    path('create/', CreateStockReceptionView.as_view(), name='create'),
    path('delete/<int:pk>/', DeleteStockReceptionView.as_view(), name='delete')
]
