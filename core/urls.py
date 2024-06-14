from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', HomeView.as_view(), name='home'),
    
    path('users/', include(('users.urls', 'users'))),
    path('products/', include(('products.urls', 'products'))),
    path('sales/', include(('sales.urls', 'sales'))),
    path('categories/', include(('categories.urls', 'categories'))),
    path('suppliers/', include(('suppliers.urls', 'suppliers'))),
    path('receptions/', include(('stock_reception.urls', 'receptions'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
