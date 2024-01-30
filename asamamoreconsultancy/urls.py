from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from dating_app import views

urlpatterns = [
            path('__debug__/', include('debug_toolbar.urls')),
            path('admin/', admin.site.urls),
            path('i18n/', include('django.conf.urls.i18n')),
            path('dating/', include('dating_app.urls')), 
            path('', views.home, name='home'),  
            path('', include('user_app.urls')), 
            path("", include('products.urls')),
            path('chat/', include('chat_app.urls')),
     
     

    ] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('dating/', include('dating_app.urls')), 
    path('', views.home, name='home'),  
    path('', include('user_app.urls')), 
    path("", include('products.urls')),
    path('chat/', include('chat_app.urls')),
    path("__reload__/", include("django_browser_reload.urls")),

)


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
