from django.urls import path
from .views import *


app_name = "rank"
urlpatterns = [
    #path('', GradeLV.as_view(), name='index'),
    path('rank1/', Rank_One.as_view(), name='rank1'),
    path('rank2/', Rank_Two.as_view(), name='rank2'),
    path('rank3/', Rank_Three.as_view(), name='rank3'),
    path('rank4/', Rank_Four.as_view(), name='rank4'),
]