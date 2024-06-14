from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from django.views import View
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.querys import fetch_items_for_user, fetch_objects_pagination
from .models import Sale
from products.models import Product

# Create your views here.

class SaleListView(LoginRequiredMixin, View):
    template_admin = 'sales/admin/list.html'
    template_employee = 'sales/employees/list.html'
    template_403 = 'components/403.html'
    
    def get_template(self, request):
        if request.user.rol == 'Admin':
            return self.template_admin
        elif request.user.rol == 'Employee':
            return self.template_employee
    
    def get_sales(self, request):
        consult = request.GET.get('search')
        user = request.user
        
        if user.rol == 'Admin':
            sales = Sale.objects.filter(Q(user=user) | Q(user__created_by_user=user))
        elif user.rol == 'Employee':
            sales = Sale.objects.filter(user=user)
            
        if consult:
            sales = sales.filter(Q(product__name__icontains=consult))
        
        return sales
    
    def get(self, request, *args, **kwargs):
        if request.user.rol in ['Admin', 'Employee']:
            page = request.GET.get('page', 1)
            sales = self.get_sales(request)
            sales, paginator = fetch_objects_pagination(page=page, objects=sales)
            return render(request, self.get_template(request), {'objects' : sales, 'paginator' : paginator})
        else:
            return render(request, self.template_403, status=403)

class CreateSaleView(LoginRequiredMixin, View):
    template_admin = 'sales/admin/create.html'
    template_employee = 'sales/employees/create.html'
    template_403 = 'components/403.html'
    
    def get_sales_products(self, request):
        return request.session.get('sales_products', [])
    
    def set_sales_products(self, request, sales_products):
        request.session['sales_products'] = sales_products
    
    def get_products(self, request):
        consult = request.GET.get('search')
        user = request.user
        products = None
        
        if consult:
            products = fetch_items_for_user(user=user, model=Product)
            products = products.filter(Q(status='Available') & (Q(code__icontains=consult) | Q(name__icontains=consult)))
        
        return products
    
    def add_product_to_sale(self, request, product, sale_amount):
        sales_products = self.get_sales_products(request)
        
        if int(sale_amount) <= product.stock:
            product.stock = int(sale_amount)
                
            for sales_product in sales_products:
                if sales_product['id'] == product.id:
                    sales_product['stock'] += product.stock
                    sales_product['total'] += product.price * product.stock
                    self.set_sales_products(request, sales_products)
                    return redirect('sales:create')
                        
            product_data = {
                'id': product.id,
                'code' : product.code,
                'name': product.name,
                'price': product.price,
                'stock': product.stock,
                'total': product.stock * product.price,
                'user_id': product.user.id
            }
            
            sales_products.append(product_data)
            self.set_sales_products(request, sales_products)
            return redirect('sales:create')
        else:
            messages.warning(request, 'Stock insuficiente')
            return redirect('sales:create')
    
    def remove_product_from_sales(self, request, sale_product_id):
        sales_products = self.get_sales_products(request)
        sales_products = [sales_product for sales_product in sales_products if sales_product['id'] != int(sale_product_id)]
        self.set_sales_products(request, sales_products)
        return redirect('sales:create')
    
    def get_total(self, request):
        sales_products = self.get_sales_products(request)
        return sum([sales_product['stock'] * sales_product['price'] for sales_product in sales_products])
    
    def get(self, request, *args, **kwargs):
        id_product = request.GET.get('id_product')
        sale_amount = request.GET.get('amount')
        sale_product_id = request.GET.get('id_sale_product')
        
        if id_product is not None:
            product = Product.objects.get(pk=id_product)
            return self.add_product_to_sale(request, product, sale_amount)
    
        if sale_product_id is not None:
            return self.remove_product_from_sales(request, sale_product_id)
        
        total = self.get_total(request)
        
        context = {
            'products': self.get_products(request),
            'sale_products': self.get_sales_products(request),
            'total': total,
        }
        
        if request.user.rol == 'Admin':
            return render(request, self.template_admin, context)
        elif request.user.rol == 'Employee':
            return render(request, self.template_employee, context)
        else:
            return render(request, self.template_403, status=403)
    
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            sales_products = self.get_sales_products(request)
            products_to_update = Product.objects.select_for_update().in_bulk(
                [sales_product['id'] for sales_product in sales_products]
            )

            for sales_product in sales_products[:]:
                product = products_to_update[sales_product['id']]
                if sales_product['stock'] > product.stock:
                    messages.warning(request, 'Stock insuficiente')
                    return redirect('sales:create')

                existing_sale_product = Sale.objects.filter(
                    product_id=sales_product['id'],
                    created_at__date=timezone.now(),
                    price_sale=sales_product['price'],
                    user=request.user
                ).first()
                
                if existing_sale_product:
                    existing_sale_product.amount_sale += sales_product['stock']
                    existing_sale_product.save()
                else:
                    Sale.objects.create(
                        user=request.user,
                        product_id=sales_product['id'],
                        amount_sale=sales_product['stock'],
                        price_sale=sales_product['price']
                    )

                product.stock -= sales_product['stock']
                product.save()
                
            self.set_sales_products(request, [])
        
        return redirect('sales:list')
    
class DeleteSaleView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        if request.user.rol == 'Admin':
            sale = fetch_items_for_user(user=request.user, model=Sale, pk=pk)

            product = Product.objects.get(id=sale.product.id)
            product.stock += sale.amount_sale
            product.save()
            
            sale.delete()
            
            return redirect('sales:list')
        else:
            return render(request, 'components/403.htm', status=403)