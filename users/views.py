from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.querys import fetch_objects_pagination
from products.models import Product
from categories.models import Category
from sales.models import Sale
from suppliers.models import Supplier
from stock_reception.models import StockReception
from .models import User, Dashboard
from .forms import UserAdminRegisterForm, LoginUserForm, UserEmployeeRegisterForm, UserEditForm,DashboardForm

class UserAdminRegisterView(View):
    template_register = 'users/register.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_register, {'form': UserAdminRegisterForm()})
    
    def post(self, request, *args, **kwargs):
        form = UserAdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Usuario Creado!!')
            return redirect('home')
        return render(request, self.template_register, {'form': form})

class UserEmployeeRegisterView(LoginRequiredMixin, View):
    template_create_user = 'users/admin/create.html'
     
    def get(self, request, *args, **kwargs):
        if request.user.rol == 'Admin':
            return render(request, self.template_create_user, {'form': UserEmployeeRegisterForm})
        else:
            return render(request, 'components/403.html', status=403)
    
    def post(self, request, *args, **kwargs):
        form = UserEmployeeRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.created_by_user = request.user
            new_user.rol = 'Employee'
            new_user.save()
            messages.success(request, 'Usuario Creado!')
            return redirect('users:list')
        return render(request, self.template_create_user, {'form': form})

class ListUsersForAdminView(LoginRequiredMixin, View):
    def get_users(self, request):
        consult = request.GET.get('search')
        user = request.user
        
        if user.rol == 'Admin':
            users = User.objects.filter(created_by_user=request.user)
        else:
            users = None
        
        if consult:
            users = users.filter(Q(email__icontains=consult) | Q(first_name__icontains=consult) | Q(last_name__icontains=consult))
        
        return users
    
    def get(self, request, *args, **kwargs):
        if request.user.rol == 'Admin':
            page = request.GET.get('page', 1)
            users = self.get_users(request)
            users, paginator = fetch_objects_pagination(page=page, objects=users)
            return render(request, 'users/admin/list.html', {'objects' : users, 'paginator' : paginator})
        else:
            return render(request, 'components/403.html', status=403)

class LoginUserView(View):
    template_login = 'users/login.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_login, {'form': LoginUserForm})
    
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        messages.warning(request, 'El usuario o la contraseña no son válidos!')
        return render(request, self.template_login, context={'form': form})

class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')

class EditUserView(LoginRequiredMixin, View):
    template_admin = 'users/admin/edit.html'
    template_employee = 'users/employees/edit.html'
    template_404 = 'components/404.html'
    
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        if request.user.rol == 'Employee':
            return self.template_employee
        else:
            return self.template_404
        
    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        template = self.get_template(request)
        
        return render(request, template, {'form': UserEditForm(instance=user, current_user=request.user)})
    
    def post(self, request, *args, **kwargs):
        template = self.get_template(request)        
        current_email = request.user.email
        form = UserEditForm(request.POST, request.POST, instance=request.user, current_user=request.user)

        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_username = form.cleaned_data.get('username')
            new_email = form.cleaned_data.get('email')
            new_password = form.cleaned_data.get('password_new')
            user = authenticate(username=current_email, password=current_password)
            if user is not None:
                if new_email and new_email != request.user.email:
                    request.user.email = new_email
                if new_password:
                    request.user.set_password(new_password)
                    update_session_auth_hash(request, request.user)
                request.user.save()
                messages.warning(request, 'Datos Actualizados')
                return redirect('home')
            else:
                messages.error(request, 'La contraseña actual no es correcta!')
                return redirect('users:edit')
        return render(request, template, context={'form': form})
                            
class DeleteUserEmployeView(LoginRequiredMixin, View):
    def save_objects_user_admin(self, request, elemets):
        for elem in elemets:
            elem.user = request.user
            elem.save()
    
    def get(self, request, pk, *args, **kwargs):
        if request.user.rol == 'Admin':
            user = get_object_or_404(User, created_by_user=request.user, pk=pk)
            products = Product.objects.filter(user=user)
            categories = Category.objects.filter(user=user)
            sales = Sale.objects.filter(user=user)
            suppliers = Supplier.objects.filter(user=user)
            stock_receptions = StockReception.objects.filter(user=user)
            
            if products:
                self.save_objects_user_admin(request, products)
            
            if categories:
                self.save_objects_user_admin(request, categories)
                    
            if sales:
                self.save_objects_user_admin(request, sales)
                
            if suppliers:
                self.save_objects_user_admin(request, suppliers)
            
            if stock_receptions:
                self.save_objects_user_admin(request, stock_receptions)
            
            user.delete()
            messages.info(request, f"El usuario {user.first_name} {user.last_name} ha sido eliminado!")
            return redirect("users:list")
        else:
            return render(request, 'components/403.html', status=403)

class DashboardAdminView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.rol == 'Admin':
            dashboard = Dashboard.objects.get(user=request.user)
            return render(request, 'users/admin/dashboard.html', {'form': DashboardForm( instance=dashboard), 'dashboard':dashboard})
        else:
            return render(request, 'components/403.html', status=403)
    
    def post(self, request, *args, **kwargs):
        dashboard = Dashboard.objects.get(user=request.user)
        form = DashboardForm(request.POST, request.FILES, instance=dashboard)
        if form.is_valid:
            form.save()
            return redirect('home')
        else:
            messages.warning(request, 'Formulario Invalido')
            return render(request, 'users/admin/dashboard.html', {'form': DashboardForm( instance=dashboard), 'dashboard':dashboard})