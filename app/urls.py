from django.urls import path
from . import views
from app import views as user_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('accounts/register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('new_post/',views.new_post,name='new_post'),
    path('search/', views.search_results, name = 'search_results'),
]

if settings.DEBUG:
       urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)