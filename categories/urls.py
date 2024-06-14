from django.urls import path

from .views import CategoryListView, CreateCategoryView, UpdateCategoryView, DeleteCategoryView

urlpatterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('create/', CreateCategoryView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateCategoryView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteCategoryView.as_view(), name='delete'),
]
