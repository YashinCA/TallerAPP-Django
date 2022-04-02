from django.urls import path
from .views import IndexView, DeleteImage, Detail, Talleres, CambioPass

app_name = 'dashboard'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('delete/<int:pk>', DeleteImage.as_view(), name="delete"),
    path('view/<int:pk>', Detail.as_view(), name="detail"),
    path('talleres', Talleres.as_view(), name="talleres"),
    path('cambiopass', CambioPass.as_view(), name="cambiopass"),
]
