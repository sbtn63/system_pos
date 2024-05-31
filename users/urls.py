from django.urls import path

from .views import (
    UserAdminRegisterView, 
    LoginUserView, 
    LogoutUserView, 
    UserEmployeeRegisterView,
    ListUsersForAdminView,
    EditUserView,
    DeleteUserEmployeView,
    DashboardAdminView,
)

urlpatterns = [
    
    path('dashboard/', DashboardAdminView.as_view(), name='dashboard'),
    
    path('register/', UserAdminRegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    
    path('new_user/', UserEmployeeRegisterView.as_view(), name='new_user'),
    path('list_users/', ListUsersForAdminView.as_view(), name='list_users'),
    path('edit_users/', EditUserView.as_view(), name='edit_user'),
    path('delete_user/<int:pk>', DeleteUserEmployeView.as_view(), name='delete_user'),
]
