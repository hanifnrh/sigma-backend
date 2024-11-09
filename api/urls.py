from django.urls import path
from .views import ParameterListCreate, ParameterDetail, DataAyamListCreate, DataAyamDetail, StartFarmingListCreate, StartFarmingDetail
urlpatterns = [
    path('parameters/', ParameterListCreate.as_view(), name='parameter-list-create'),
    path('parameters/<int:pk>/', ParameterDetail.as_view(), name='parameter-detail'),
    
    path('data-ayam/', DataAyamListCreate.as_view(), name='data-ayam-list-create'),
    path('data-ayam/<int:pk>/', DataAyamDetail.as_view(), name='data-ayam-detail'),
    
    path('start-farming/', StartFarmingListCreate.as_view(), name='start-farming'),
    path('start-farming/<int:pk>/', StartFarmingDetail.as_view(), name='start-farmingdetail'),
]
