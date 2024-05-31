from django.shortcuts import render, get_list_or_404
from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import User, Dashboard

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.rol == 'Admin':
            dashoard = Dashboard.objects.get(user=request.user)
            return render(request, 'core/admin/home.html')
        if request.user.rol == 'Employee':
            return render(request, 'core/employee/home.html')
        else:
            return render(request, 'components/404.html')