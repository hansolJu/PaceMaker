from django.urls import path, re_path
from .views import *

app_name='course'
urlpatterns = [
    path('diagram/', DiagramTV.as_view(), name='diagram'),
]