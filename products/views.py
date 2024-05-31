from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Product
from .forms import ProductForm, ProductUpdateForm
from categories.models import Category
# Create your views here.

class ListProductsView(LoginRequiredMixin, View):
    template_admin = 'products/admin/list.html'
    template_employee = 'products/employees/list.html'
    template_404 = 'components/404.html'

    def get_products(self, request):
        consult = request.GET.get('search')
        user = request.user

        if user.rol == 'Admin': 
            products = Product.objects.filter(Q(user=user) | Q(user__created_by_user=user))
        elif user.rol == 'Employee': 
            products = Product.objects.filter(Q(user=user.created_by_user) | Q(user__created_by_user=user.created_by_user))
        else: 
            products = None
        
        if consult: 
            products = products.filter(Q(name__icontains=consult) | Q(code__icontains=consult))

        return products

    def get(self, request, *args, **kwargs):
        products = self.get_products(request)
        if products is None: 
            return render(request, self.template_404)
        elif request.user.rol == 'Admin': 
            return render(request, self.template_admin, {'products': products})
        elif request.user.rol == 'Employee': 
            return render(request, self.template_employee, {'products': products})

class CreateProductView(LoginRequiredMixin, View):
    template_admin = 'products/admin/create.html'
    template_employee = 'products/employees/create.html'
    template_404 = 'components/404.html'

    def get_products(self, request):
        user = request.user

        if user.rol == 'Admin': 
            products = Product.objects.filter(Q(user=user) | Q(user__created_by_user=user))
        elif user.rol == 'Employee': 
            products = Product.objects.filter(Q(user=user.created_by_user) | Q(user__created_by_user=user.created_by_user))
        else: 
            products = None

        return products
    
    def get_form(self, request, form):
        user = request.user

        if user.rol == 'Admin':
            form.fields['category'].queryset = Category.objects.filter(Q(user=user) | Q(user__created_by_user=user)) 
        elif user.rol == 'Employee': 
            form.fields['category'].queryset = Category.objects.filter(Q(user=user.created_by_user) | Q(user__created_by_user=user.created_by_user))

        return form

    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
        else:
            return self.template_404

    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, self.get_template(request), {'form': self.get_form(request, form)})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            
            products = self.get_products(request)

            for product in products:
                if product.code == new_product.code:
                    messages.warning(request, f'El código {product.code} ya tiene un producto asociado')
                    return render(request, self.get_template(request), {'form': form})

            new_product.user = request.user
            new_product.save()
            messages.success(request, f'Producto {new_product.name} con código {new_product.code} fue creado')
            return redirect('products:list_products')

        else:
            messages.warning(request, 'Formulario inválido')
            return render(request, self.get_template(request), {'form': form})
    
class UpdateProductAdminView(LoginRequiredMixin, View):
    template_update = 'products/admin/update.html'
    template_404 = 'components/404.html'

    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_update
        else:
            return self.template_404

    def get(self, request, pk, *args, **kwargs):
        template = self.get_template(request)
        product = get_object_or_404(Product, Q(user=request.user) | Q(user__created_by_user=request.user), pk=pk)
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(Q(user=request.user) | Q(user__created_by_user=request.user))
        return render(request, template, {'form': form})

    def post(self, request, pk, *args, **kwargs):
        template = self.get_template(request)
        product = get_object_or_404(Product, Q(user=request.user) | Q(user__created_by_user=request.user), pk=pk)
        form = ProductUpdateForm(request.POST or None, instance=product)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado')
            return redirect('products:list_products')
        else:
            messages.warning(request, 'Formulario inválido')
            return render(request, template, {'form': form})

class DeleteProductAdminView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.rol == 'Admin':
            product = get_object_or_404(Product, Q(user=request.user) | Q(user__created_by_user=request.user), pk=pk)
            product.delete()
            messages.warning(request, f'El producto {product.name} con codigo {product.code} fue eliminado')
            return redirect('products:list_products')
        else:          
            return render(request, 'components/404.html')
