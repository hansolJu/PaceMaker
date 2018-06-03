from django.urls import path, re_path
from .views import *

app_name='course'
urlpatterns = [
    path('diagram/', diagramBV.as_view(), name= 'diagram'),
]