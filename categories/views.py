from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.querys import fetch_items_for_user
from .models import Category
from .forms import CategoryForm, CategoryUpdateForm


# Create your views here.

class CategoryListView(LoginRequiredMixin, View):
    template_admin = 'categories/admin/list.html'
    template_employee = 'categories/employee/list.html'
    template_404 = 'components/404.html'
    
    def get_categories(self, request):
        consult = request.GET.get('search')
        user = request.user
        
        categories = fetch_items_for_user(user=user, model=Category)
        
        if consult: 
            categories = categories.filter(Q(name__icontains=consult) | Q(location__icontains=consult))
        
        return categories
             
    def get(self, request, *args, **kwargs):
        categories = self.get_categories(request)
        
        if categories is None:
            return render(request, self.template_404)
        elif request.user.rol == 'Admin':
            return render(request, self.template_admin, {'categories': categories})
        elif request.user.rol == 'Employee':
            return render(request, self.template_employee, {'categories': categories})

class CreateCategoryView(LoginRequiredMixin, View):
    template_admin = 'categories/admin/create.html'
    template_employee = 'categories/employee/create.html'
    template_404 = 'categories/404.html'
        
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
        else:
            return self.template_404
    
    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        return render(request, self.get_template(request), {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            
            categories = fetch_items_for_user(user=request.user, model=Category)

            for category in categories:
                if category.code == new_category.code:
                    messages.warning(request, f'El código {category.code} ya tiene una categoria asociada')
                    return render(request, self.get_template(request), {'form': form})

            new_category.user = request.user
            new_category.save()
            messages.success(request, f'Categoria {new_category.name} con código {new_category.code} fue creada')
            return redirect('categories:list_categories')

        else:
            messages.warning(request, 'Formulario inválido')
            return render(request, self.get_template(request), {'form': form})

class UpdateCategoryView(LoginRequiredMixin, View):
    template_update = 'categories/admin/update.html'
    template_404 = 'categories/404.html'
    
    def get_template(self, request):
        user = request.user
        
        if user.rol == 'Admin':
            return self.template_update
        else:
            return self.template_404
    
    def get(self, request, pk, *args, **kwargs):
        template = self.get_template(request)
        category = fetch_items_for_user(user=request.user, model=Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(request, template, {'form': form})
    
    def post(self, request, pk, *args, **kwargs):
        template = self.get_template(request)
        category = fetch_items_for_user(user=request.user, model=Category, pk=pk)
        form = CategoryUpdateForm(request.POST or None, instance=category)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria Actualizada')
            return redirect('categories:list_categories')
        else:
            messages.warning(request, 'Formulario invalido')
            return render(request, template, {'form': form})

class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.rol == 'Admin':
            category = fetch_items_for_user(user=request.user, model=Category, pk=pk)
            category.delete()
            messages.success(request, f'La categoria {category.name} con el codigo {category.code} fue eliminada')
            return redirect('categories:list_categories')
        else:
            return render(request, 'components/404.html')