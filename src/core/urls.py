from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('', include('main.urls')),
    path('', include('accounts.urls')),
    path('api/', include('api.urls')),

    path('admin/', admin.site.urls),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
