from django.urls import path
from . import views

urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('new-post/',views.new_post,name='new-post'),
]