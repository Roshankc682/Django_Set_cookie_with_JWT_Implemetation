from django.conf.urls import url
from django.urls import path , include

urlpatterns = [
    path('', include('first_app.urls'))
]
