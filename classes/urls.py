from django.urls import path, re_path
from .views import *

app_name='classes'
urlpatterns = [
    path('list/', majorLV.as_view(), name= 'major_list'),
    path('recommand/', RecommandView.as_view(), name= 'recommand'),
    re_path(r'^(?P<pk>\d+)/$', majorDV.as_view(), name='major_detail'),
]