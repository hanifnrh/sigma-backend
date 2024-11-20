from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    ParameterListCreate,
    ParameterDetail,
    DataAyamListCreate,
    DataAyamDetail,
    get_data_ayam_history,
)
urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), 
    
    path('parameters/', ParameterListCreate.as_view(), name='parameter-list-create'),
    path('parameters/<int:pk>/', ParameterDetail.as_view(), name='parameter-detail'),
    
    path('data-ayam/', DataAyamListCreate.as_view(), name='data-ayam-list-create'),
    path('data-ayam/<int:pk>/', DataAyamDetail.as_view(), name='data-ayam-detail'),
    
    path('data-ayam/<int:pk>/history/', get_data_ayam_history, name='data-ayam-history'),
]
