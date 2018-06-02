from django.urls import path
from .views import *


app_name = "grades"
urlpatterns = [
    #path('', GradeLV.as_view(), name='index'),
    path('total_grade/', GradeLV.as_view(), name='total'),
    path('semester_grade/', SemesterGradeLV.as_view(), name='semester'),
    path('major_grade/', MajorGradeLV.as_view(), name='major'),
    path('ge_grade/', GeGradeLV.as_view(), name='ge'),
    path('msc_grade/',MscGradeLV.as_view(), name='msc'),
]
