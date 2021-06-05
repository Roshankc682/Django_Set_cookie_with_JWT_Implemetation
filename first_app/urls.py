from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

# make a env file and import all requirements
urlpatterns = [
    path('register/',views.RegisterView.as_view(), name='Register_account'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='Token_create'),
    path('api/token/new/', views.user_new_access_and_refrsh_token_and, name='Token_refresh_of_reflecting_acces_token'),
    path('api/access/refresh/', TokenRefreshView.as_view(), name='Get_access_if_page_refresh'),
    path('api/logout', views.logout, name='Logout'),
    path('api/dashboard/', views.get_data_of_user, name='Token_create'),
]