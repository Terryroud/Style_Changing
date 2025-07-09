from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('main_ai/', views.transfer_style_view, name='main_ai'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
