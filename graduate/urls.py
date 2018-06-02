from django.urls import path
from .views import *


app_name = "graduate"
urlpatterns = [
    path('graduate_certificate/', GraduateLV.as_view(), name='graduate_confirm'),
]
