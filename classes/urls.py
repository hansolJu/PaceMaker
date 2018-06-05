from django.urls import path, re_path
from .views import *

app_name='classes'
urlpatterns = [
    path('list/', majorLV.as_view(), name= 'major_list'),
    re_path(r'^(?P<pk>\d+)/$', majorDV.as_view(), name='major_detail'),

    path('retake/', RetakeRecommandView.as_view(), name= 'retake'),
    path('special/', SpecialCourseRecommandView.as_view(), name= 'special'),
    path('top/', TopStudentRecommandView.as_view(), name= 'top'),
    path('pre/', preCourseRecommandView.as_view(), name= 'pre'),
]