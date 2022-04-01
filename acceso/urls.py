from django.urls import path, re_path
from .views import LoginView, login, logout, welcome, Talleres, Detail

from . import views

app_name = 'acceso'

urlpatterns = [
    path('', welcome, name='bienvenida'),
    path('acceso/', LoginView.as_view(), name='acceso'),
    path('talleres/', Talleres.as_view(), name='talleres'),
    path('view/<int:pk>', Detail.as_view(), name="detail"),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
