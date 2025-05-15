# sigma_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse

def redirect_to_site_login(request):
    return HttpResponseRedirect("https://www.sigma-ta.com/")

def health_check(request):
    return JsonResponse({'status': 'ok'}, status = 200)


urlpatterns = [
    path('', redirect_to_site_login),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include api app URLs
    path('health/', health_check),
] 
