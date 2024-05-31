from users.models import Dashboard

def dashboard_user_context(request):
    if request:
        try:
            if request.user.rol == 'Admin':
                dashboard =  Dashboard.objects.get(user=request.user)
            
            elif request.user.rol == 'Employee':
                dashboard =  Dashboard.objects.get(user=request.user.created_by_user)
            return {
                'dashboard': dashboard
            }
        except Exception:
            return {
                'dashboard': ''
            }