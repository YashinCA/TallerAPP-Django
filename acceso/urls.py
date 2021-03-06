from django.urls import path, re_path
from .views import LoginView, forgetpassword, login, logout, welcome, Talleres, Detail
from decorator_include import decorator_include
from acceso.utils.decoradores import login_requerido
from django.urls import include

from . import views

app_name = 'acceso'

urlpatterns = [
    path('', welcome, name='bienvenida'),
    path('acceso/', LoginView.as_view(), name='acceso'),
    path('talleres', Talleres.as_view(), name="talleres"),
    path('view/<int:pk>', Detail.as_view(), name="detail"),
    path('login/', login, name='login'),
    path('forget_password/', forgetpassword, name='forgetpassword'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('restore_password/<uidb64>/<token>/',
         views.restore_password, name='restore_password'),
]
