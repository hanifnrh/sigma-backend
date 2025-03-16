# sigma_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def redirect_to_site_login(request):
    return("https://www.sigma-ta.com/")



urlpatterns = [
    path('', redirect_to_site_login),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include api app URLs
] 
