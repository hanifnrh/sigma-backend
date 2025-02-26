from django.urls import path
#from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    ParameterListCreate,
    ParameterDetail,
    DataAyamListCreate,
    DataAyamDetail,
    DataAyamHistoryList,
    LoginView,
    RegisterView,
)
urlpatterns = [
    #path('api-token-auth/', obtain_auth_token, name='api_token_auth'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('parameters/', ParameterListCreate.as_view(), name='parameter-list-create'),
    path('parameters/<int:pk>/', ParameterDetail.as_view(), name='parameter-detail'),
    
    path('data-ayam/', DataAyamListCreate.as_view(), name='data-ayam-list-create'),
    path('data-ayam/<int:pk>/', DataAyamDetail.as_view(), name='data-ayam-detail'),
    
    path('data-ayam/<int:pk>/history/', DataAyamHistoryList.as_view(), name='data-ayam-history'),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),

]
