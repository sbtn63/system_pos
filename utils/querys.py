from django.db.models import Q
from django.shortcuts import get_object_or_404

def fetch_items_for_user(user, model, pk=None):
    """
    Retrieves items for a given user from the specified model.

    Args:
    user (User): The user requesting the items.
    model (Model): The Django model from which to retrieve items.
    pk (int, optional): The primary key of a specific item to retrieve. Defaults to None.

    Returns:
    QuerySet or Model instance: A queryset of items or a single item instance if pk is provided.
    """
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