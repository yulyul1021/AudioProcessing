from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from audioProcessing import views

urlpatterns = [
    path('main', views.main, name='main'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
