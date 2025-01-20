
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from . import settings
from boutique.views import accueil, ajout_au_panier
import os

urlpatterns = [
    path('', accueil),
    path('medard/admin/', admin.site.urls),
    url(r'ckeditor/', include('ckeditor_uploader.urls')),
    path('ajout_au_panier/', ajout_au_panier, name='ajout_au_panier'),
    path('boutique/', include('boutique.urls', namespace='boutique')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns=[
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

