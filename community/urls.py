from django.urls import path, re_path

from community.views import *

app_name = 'community'

urlpatterns = [
    # # ex: /blog/
    # path('', PostLV.as_view(), name='index'),

    # ex: /post/
    path('post/', PostLV.as_view(), name='post_list'),

    # ex: /post/django-example/
    #path('<int:pk>/<slug:slug>/',PostDV.as_view(),name ='post_detail'),
    # re_path(r'^<int:pk>/(?P<slug>[-\w]+)/$', PostDV.as_view(), name='post_detail'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', PostDV.as_view(), name = 'post_detail'),

    # /add/
    path('add/', PostCreateView.as_view(), name="add",),

    # /99/update/
    path('<int:pk>/change/', PostUpdateView.as_view(), name="update",),

    # /99/delete/
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="delete",),
]