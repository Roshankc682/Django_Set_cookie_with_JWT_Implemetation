from django.conf.urls import url
from django.urls import path , include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('', include('first_app.urls')),
    url(r'^image/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)