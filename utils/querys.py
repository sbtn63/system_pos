from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404

def fetch_items_for_user(user, model, pk=None):
    if pk is None:
        if user.rol == 'Admin':
            return model.objects.filter(Q(user=user) | Q(user__created_by_user=user))    
        elif user.rol == 'Employee': 
            return  model.objects.filter(Q(user=user.created_by_user) | Q(user__created_by_user=user.created_by_user))
        else:
            return None  
    else:
        if user.rol == 'Admin':
            return get_object_or_404(model, Q(user=user) | Q(user__created_by_user=user), pk=pk)

def fetch_objects_pagination(page, objects):
        try:
            paginator = Paginator(objects, 5)
            objects = paginator.page(page)
            
            return objects, paginator
        except:
            raise Http404