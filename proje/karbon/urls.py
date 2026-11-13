from django.urls import path #url tanımlama
from . import views #views.py dosyası çağrılır

#url'lerin tutulduğu yer
urlpatterns = [
    path('',views.homepage,name=""),
    path('register',views.register,name="register"),
    path('login',views.my_login,name='login'),
    path('hesaplama',views.hesaplama,name='hesaplama'),
    path('user-logout',views.user_logout,name='user-logout'),
    path('bilgilerim', views.bilgilerim, name='bilgilerim'),
    path('sifre-degistir', views.sifre_degistir, name='sifre-degistir'),
    
]
