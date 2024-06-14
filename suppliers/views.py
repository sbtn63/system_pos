from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.querys import fetch_items_for_user, fetch_objects_pagination
from .models import Supplier
from .forms import SupplierForm

# Create your views here.

class ListSupplierView(LoginRequiredMixin, View):
    template_admin = 'suppliers/admin/list.html'
    template_employee = 'suppliers/employees/list.html'
    template_403 = 'components/403.html'
    
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
    
    def get_suppliers(self, request):
        consult = request.GET.get('search')
        user = request.user
        
        suppliers = fetch_items_for_user(user=user, model=Supplier)
        
        if consult:
            suppliers = suppliers.filter(Q(document__icontains=consult) | Q(name__icontains=consult))
        
        return suppliers
    
    def get(self, request, *args, **kwargs):
        if request.user.rol in ['Admin', 'Employee']:
            page = request.GET.get('page', 1)
            suppliers = self.get_suppliers(request)
            suppliers, paginator = fetch_objects_pagination(page=page, objects=suppliers)
            return render(request, self.get_template(request), {'objects' : suppliers, 'paginator' : paginator})
        else:
            return render(request, self.template_403, status=403)

class CreateSupplierView(LoginRequiredMixin, View):
    template_admin = 'suppliers/admin/create.html'
    template_employee = 'suppliers/employees/create.html'
    template_403 = 'components/403.html'
    
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
    
    def get(self, request, *args, **kwargs):
        if request.user.rol not in ['Admin', 'Employee']:
            return render(request, self.template_403, status=403)
        
        form = SupplierForm()
        return render(request, self.get_template(request), {'form' : form})
    
    def post(self, request, *args, **kwargs):
        form = SupplierForm(request.POST)
        
        if form.is_valid():
            new_supplier = form.save(commit=False) 
            
            suppliers = fetch_items_for_user(user=request.user, model=Supplier)
            
            for supplier in suppliers:
                if new_supplier.document == supplier.document:
                    messages.warning(request, f'El documento {new_supplier.document} ya esta asociado a un provedor')
                    return render(request, self.get_template(request), {'form' : form})
                
                if new_supplier.email == supplier.email:
                    messages.warning(request, f'El email {new_supplier.email} ya esta asociado a un provedor')
                    return render(request, self.get_template(request), {'form' : form})
            
            new_supplier.user = request.user
            new_supplier.save()
            messages.success(request, f'EL provedor {new_supplier.name} con dni o nit {new_supplier.document} fue creado')
            return redirect('suppliers:list')
        
        else:
            messages.warning(request, f'Formulario invalido')
            return render(request, self.get_template(request), {'form' : form})
            
class UpdateSupplierView(LoginRequiredMixin, View):
    template_admin = 'suppliers/admin/edit.html'
    template_403 = 'components/403.html'
    
    def get_supliers(self, request, pk):
        if request.user.rol == 'Admin':
            suppliers = Supplier.objects.filter(Q(user=request.user) | Q(user__created_by_user=request.user), ~Q(id=pk))
        else:
            suppliers = None
        
        return suppliers
    
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
    
    def get(self, request, pk, *args, **kwargs):
        if not request.user.rol == 'Admin':
            return render(request, self.template_403, status=403)
        
        supplier = fetch_items_for_user(user=request.user, model=Supplier, pk=pk)
        form = SupplierForm(instance=supplier)
        return render(request, self.get_template(request), {'form' : form})
    
    def post(self, request, pk, *args, **kwargs):
        supplier = fetch_items_for_user(user=request.user, model=Supplier, pk=pk)
        form = SupplierForm(request.POST, instance=supplier)
        
        if form.is_valid():
            update_supplier = form.save(commit=False) 
            
            suppliers = self.get_supliers(request, pk)
            
            for supplier in suppliers:
                if update_supplier.document == supplier.document:
                    messages.warning(request, f'El documento {update_supplier.document} ya esta asociado a un provedor')
                    return render(request, self.get_template(request), {'form' : form})
                
                if update_supplier.email == supplier.email:
                    messages.warning(request, f'El email {update_supplier.email} ya esta asociado a un provedor')
                    return render(request, self.get_template(request), {'form' : form})
            
            update_supplier.save()
            messages.success(request, f'EL provedor {update_supplier.name} con dni o nit {update_supplier.document} fue actualizado')
            return redirect('suppliers:list')
        
        else:
            messages.warning(request, f'Formulario invalido')
            return render(request, self.get_template(request), {'form' : form})

class DeleteSupplierView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.rol == 'Admin':
            supplier = fetch_items_for_user(user=request.user, model=Supplier, pk=pk)
            supplier.delete()
            messages.success(request, f'El provedor {supplier.name} con el documento o nit {supplier.document} fue eliminado')
            return redirect('suppliers:list')
        else:
            return render(request, 'components/403.html', status=403)