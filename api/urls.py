from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('all_twits/', views.all_twits, name='all_twits'),
    path('login/', views.darius_login, name='login'),
    path('logout/', views.darius_logout, name='logout'),
    path('save_pic/', views.save_pic, name='save_pic'),
    path('save_twits/', views.save_twits, name='save_twits'),
    path('user_register/', views.user_register, name='user_register'),
    path('login_page/', views.login_page, name='login_page'),
    #path(r'login_page/?next=([a-zA-Z0-9/]*)', views.login_fix, name='login_fix'),
]