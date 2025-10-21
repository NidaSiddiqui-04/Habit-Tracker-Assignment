from django.urls import path
from . import views
from . views import CustomLoginView
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as a_views

app_name='user_profile'
urlpatterns=[
    path('register/',views.register,name='register'),
    path('',CustomLoginView.as_view(template_name='user_profile/login.html'),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('add_user_profile/',views.add_user_profile,name='add_user_profile'),
    path('profile_view/',views.detail_page,name='detail_view')
]