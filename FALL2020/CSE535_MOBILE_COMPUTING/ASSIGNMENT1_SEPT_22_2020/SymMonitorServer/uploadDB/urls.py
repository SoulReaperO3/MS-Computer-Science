from django.conf.urls import url
from .views import FileView
from django.urls import path

urlpatterns = [
    url(r'^upload/$', FileView.as_view(), name='file-upload'),
]
