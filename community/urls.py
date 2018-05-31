from django.urls import path, re_path

from community.views import *

app_name = 'community'

urlpatterns = [
    # # ex: /community/
    # path('', PostLV.as_view(), name='index'),

    # ex: /community/post_oldbook/
    path('post_oldbook/', OldbookLV.as_view(), name='post_ob'),

    # ex: /community/post_information/
    path('post_information/', InfoLV.as_view(), name='post_Info'),

    # ex: /community/post_Info/
    path('post_Info/', SearchFormView.as_view(), name='Info_list'),

    # ex: /community/post_ob/
    path('post_ob/', OBSearchFormView.as_view(), name='ob_list'),

    # ex: /Info/django-example/
    re_path(r'^Info/(?P<slug>[-\w]+)/$', PostDV.as_view(), name = 'Info_detail'),

    # ex: /Info/django-example/
    re_path(r'^ob/(?P<slug>[-\w]+)/$', OBPostDV.as_view(), name = 'ob_detail'),

    # post_Info/add/
    path('post_Info/add/', PostCreateView.as_view(), name="Info_add"),

    # post_ob/add/
    path('post_ob/add/', OBPostCreateView.as_view(), name="ob_add"),

    # /99/update/
    path('post_Info/<int:pk>/change/', PostUpdateView.as_view(), name="Info_update"),

    # /99/update/
    path('post_ob/<int:pk>/change/', OBPostUpdateView.as_view(), name="ob_update"),

    # /99/delete/
    path('post_Info/<int:pk>/delete/', PostDeleteView.as_view(), name="Info_delete"),

    # /99/delete/
    path('post_ob/<int:pk>/delete/', OBPostDeleteView.as_view(), name="ob_delete"),
]