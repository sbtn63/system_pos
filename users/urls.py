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
    
    path('new/', UserEmployeeRegisterView.as_view(), name='new'),
    path('list/', ListUsersForAdminView.as_view(), name='list'),
    path('edit/', EditUserView.as_view(), name='edit'),
    path('delete/<int:pk>', DeleteUserEmployeView.as_view(), name='delete'),
]
