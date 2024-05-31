from django.urls import path

from .views import CategoryListView, CreateCategoryView, UpdateCategoryView, DeleteCategoryView

urlpatterns = [
    path('', CategoryListView.as_view(), name='list_categories'),
    path('create/', CreateCategoryView.as_view(), name='create_category'),
    path('update/<int:pk>/', UpdateCategoryView.as_view(), name='update_category'),
    path('delete/<int:pk>/', DeleteCategoryView.as_view(), name='delete_category'),
]
