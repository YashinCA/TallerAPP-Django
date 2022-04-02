from django.urls import path
from .views import IndexView, DeleteImage, Detail, Talleres, CambioPass
from decorator_include import decorator_include
from acceso.utils.decoradores import login_requerido
from django.urls import include

app_name = 'dashboard'

urlpatterns = [
    path('', login_requerido(IndexView.as_view()), name="index"),
    path('delete/<int:pk>', DeleteImage.as_view(), name="delete"),
    path('view/<int:pk>', Detail.as_view(), name="detail"),
    path('talleres', login_requerido(Talleres.as_view()), name="talleres"),
    #path('talleres', Talleres.as_view(), name="talleres"),
    #REFERENCIA path('dashboard/',  decorator_include(login_requerido, include('core.urls'))),
    path('cambiopass', CambioPass.as_view(), name="cambiopass"),
]
