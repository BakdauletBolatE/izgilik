
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

def asda(request):
    return "a"

urlpatterns = [
    path('',asda)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)