from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transfer/', views.transfer_style_view, name='transfer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)