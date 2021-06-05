from django.urls import path
from . import views
from .views import *
# from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

# make a env file and import all requirements
urlpatterns = [
    path('register/',views.RegisterView.as_view(), name='Register_account'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='Token_create'),
    path('api/dashboard/', views.get_data_of_user, name='Token_create'),
    path('api/logout', views.logout, name='Logout'),
]