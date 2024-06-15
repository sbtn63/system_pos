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
        if request.POST['password1'] == request.POST['password2']:
            try:
                new_admin_user = User.objects.create_user(
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                    
                new_admin_user.save()
                login(request, new_admin_user)
                    
                messages.success(request, 'User Created')
                return redirect('home')
            except IntegrityError:
                messages.warning(request, 'Email exists')
                return render(request, self.template_register, {'form': UserAdminRegisterForm})
        else:
            messages.warning(request, 'Password not match')
            return render(request, self.template_register, {'form': UserAdminRegisterForm})

class UserEmployeeRegisterView(LoginRequiredMixin, View):
    template_create_user = 'users/admin/create.html'
     
    def get(self, request, *args, **kwargs):
        if request.user.rol == 'Admin':
            return render(request, self.template_create_user, {'form': UserEmployeeRegisterForm})
        else:
            return render(request, 'components/403.html', status=403)
    
    def post(self, request, *args, **kwargs):
        form = UserEmployeeRegisterForm(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                new_employee_user = User.objects.create_user(
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email=request.POST['email'],
                    rol= 'Employee',
                    created_by_user= request.user,
                    password=request.POST['password1']
                )
                    
                new_employee_user.save()
                messages.success(request, 'Usuario Creado!')
                return redirect('users:list')
            except IntegrityError:
                messages.warning(request, 'Email exists')
                return render(request, self.template_create_user, {'form': UserEmployeeRegisterForm})
        else:
            messages.warning(request, 'Password not match')
            return render(request, self.template_create_user, {'form': UserEmployeeRegisterForm})

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
        form = LoginUserForm(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            
        if user is None:
            messages.warning(request, 'Email or pasword incorrect')
            return render(request, self.template_login, {'form': LoginUserForm})
        else:
            login(request, user)
            return redirect('home')

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
        
        return render(request, template, {'form': UserEditForm(instance=user)})
    
    def post(self, request, *args, **kwargs):
        user_form = User.objects.get(email=request.user.email)
        current_password = request.POST['current_password']
        new_password = request.POST['password_new']
        template = self.get_template(request)
                
        user = authenticate(username=request.user.email, password=current_password)
                
        if user is not None:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
                
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                    
            user.save()
            messages.warning(request, 'Datos Actualizados')
            return redirect('home')
        else:
            messages.warning(request, 'Las contrasenia no es correcta')
            return render(request, template, {'form': UserEditForm(instance=user_form)})
                    
                
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