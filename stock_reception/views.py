from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views import View
from django.contrib import messages

from .models import StockReception
from .forms import StockReceptionForm
from utils.querys import fetch_objects_pagination, fetch_items_for_user
from products.models import Product
from suppliers.models import Supplier
# Create your views here.

class ListStockReceptionView(View):
    template_admin = 'stock_reception/admin/list.html'
    template_employee = 'stock_reception/employees/list.html'
    template_403 = 'componets/403.html'
    
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
    
    def get_stock_receptions(self, request):
        consult = request.GET.get('search')
        user = request.user
        
        if user.rol == 'Admin':
            stock_receptions = StockReception.objects.filter(Q(user=user) | Q(user__created_by_user=user))
        elif user.rol == 'Employee':
            stock_receptions = StockReception.objects.filter(user=user)
        
        if consult:
            stock_receptions = stock_receptions.filter(Q(product__name__icontains=consult) | Q(supplier__name__icontains=consult))
        
        return stock_receptions
    
    def get(self, request, *args, **kwgars):
        if request.user.rol in ['Admin', 'Employee']:
            page = request.GET.get('page', 1)
            stock_receptions = self.get_stock_receptions(request)
            stock_receptions, paginator = fetch_objects_pagination(page=page, objects=stock_receptions)
            return render(request, self.get_template(request), {'objects' : stock_receptions, 'paginator' : paginator})
        else:
            return render(request, self.template_403, status=403)

class CreateStockReceptionView(View):
    template_admin = 'stock_reception/admin/create.html'
    template_employee = 'stock_reception/employees/create.html'
    template_403 = 'componets/403.html'
    
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
    
    def get(self, request, *args, **kwargs):
        if request.user.rol in ['Admin', 'Employee']:
            form = StockReceptionForm()
            form.fields['product'].queryset = fetch_items_for_user(user=request.user, model=Product)
            form.fields['supplier'].queryset = fetch_items_for_user(user=request.user, model=Supplier)
            return render(request, self.get_template(request), {'form' : form})
        else:
            return render(request, self.template_403, status=403)
    
    def post(self, request, *args, **kwargs):
        form = StockReceptionForm(request.POST)
        if form.is_valid():
            new_stock_reception = form.save(commit=False)
            new_stock_reception.user = request.user
            try:
                with transaction.atomic():
                    new_stock_reception.save()
                    product = product = get_object_or_404(Product, pk=new_stock_reception.product.id)
                    product.stock += new_stock_reception.quantity_received
                    product.save()
            except Product.DoesNotExist:
                messages.warning(request, 'El producto no existe')
                return render(request, self.get_template(request), {'form': form})
            messages.success(request, f"Recepción agregada del producto {new_stock_reception.product.name}")
            return redirect("receptions:list")
        else:
            messages.warning(request, 'Formulario inválido')
            return render(request, self.get_template(request), {'form': form})

class DeleteStockReceptionView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.rol == 'Admin':
            stock_reception = fetch_items_for_user(user=request.user, model=StockReception, pk=pk)
            
            try:
                with transaction.atomic():
                    stock_reception.delete()
                    product = product = get_object_or_404(Product, pk=stock_reception.product.id)
                    product.stock -= stock_reception.quantity_received
                    product.save()
            except Product.DoesNotExist:
                messages.warning(request, 'El producto no existe')
                
            messages.success(request, f'La recepcion del procusto {stock_reception.product.name}fue eliminada')
            return redirect('receptions:list')
        else:
            return render(request, 'components/403.html', status=403)