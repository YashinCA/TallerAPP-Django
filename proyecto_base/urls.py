
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from decorator_include import decorator_include
from acceso.utils.decoradores import login_requerido

urlpatterns = [
    path('dashboard/',  decorator_include(login_requerido, include('core.urls'))),
    path('', include('acceso.urls')),
    path('verification/', include('verify_email.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
##################