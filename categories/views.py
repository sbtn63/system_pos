from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.querys import fetch_items_for_user, fetch_objects_pagination
from .models import Category
from .forms import CategoryForm, CategoryUpdateForm


# Create your views here.

class CategoryListView(LoginRequiredMixin, View):
    template_admin = 'categories/admin/list.html'
    template_employee = 'categories/employee/list.html'
    template_403 = 'components/403.html'
    
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
    
    def get_categories(self, request):
        consult = request.GET.get('search')
        user = request.user
        
        categories = fetch_items_for_user(user=user, model=Category)
        
        if consult: 
            categories = categories.filter(Q(name__icontains=consult) | Q(location__icontains=consult))
        
        return categories
             
    def get(self, request, *args, **kwargs):
        if request.user.rol in ['Admin', 'Employee']:
            page = request.GET.get('page', 1)
            categories = self.get_categories(request)
            categories, paginator = fetch_objects_pagination(page=page, objects=categories)
            return render(request, self.get_template(request), {'objects' : categories, 'paginator' : paginator})
        else:
            return render(request, self.template_403, status=403)

class CreateCategoryView(LoginRequiredMixin, View):
    template_admin = 'categories/admin/create.html'
    template_employee = 'categories/employee/create.html'
    template_403 = 'categories/403.html'
        
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
    
    def get(self, request, *args, **kwargs):
        if request.user.rol not in ['Admin', 'Employee']:
            return render(request, self.template_403, status=403)
        
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
    template_403 = 'components/403.html'
    
    def get_template(self, request):
        user = request.user
        if user.rol == 'Admin':
            return self.template_update
    
    def get(self, request, pk, *args, **kwargs):
        if not request.user.rol == 'Admin':
            return render(request, self.template_403, status=403)
        
        template = self.get_template(request)
        category = fetch_items_for_user(user=request.user, model=Category, pk=pk)
        form = CategoryForm(instance=category)
        
        return render(request, template, {'form': form})
    
    def post(self, request, pk, *args, **kwargs):
        template = self.get_template(request)
        category = fetch_items_for_user(user=request.user, model=Category, pk=pk)
        form = CategoryUpdateForm(request.POST, instance=category)
        
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
            return render(request, 'components/403.html', status=403)