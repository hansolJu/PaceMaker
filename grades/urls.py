from django.urls import path
from .views import *


app_name = "grades"
urlpatterns = [
    #path('', GradeLV.as_view(), name='index'),
    path('semester_grade/', GradeLV.as_view(), name='semester'),
    path('major_grade/', MajorGradeLV.as_view(), name='major'),
    path('ge_grade/', GeGradeLV.as_view(), name='ge'),
    # path('post/<slug:slug>', PostDV.as_view(), name='post_detail'),
    # path('archive/', PostAV.as_view(), name='post_archive'),
    # path('<int:year>', PostAV.as_view(), name='post_year_archive'),
    # path('<int:year>/<int:month>/', PostMAV.as_view(), name='post_month_archive'),
    # path('<int:year>/<int:month>/<int:day>', PostDAV.as_view(), name='post_day_archive'),
    # path('today/', PostAV.as_view(), name='post_today_archive'),

]
