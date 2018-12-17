from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all_twits', views.all_twits, name='all_twits'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('save_pic', views.save_pic, name='save_pic'),
    path('save_twits', views.save_twits, name='save_twits'),
    path('user_register', views.user_register, name='user_register'),
]