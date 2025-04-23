# sigma_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import HttpResponseRedirect

def redirect_to_site_login(request):
    return HttpResponseRedirect("https://www.sigma-ta.com/")



urlpatterns = [
    path('', redirect_to_site_login),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include api app URLs
    path('__debug__/', include('debug_toolbar.urls'))
] 
