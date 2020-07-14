from django.conf.urls import url
from . import views


app_name = 'boutique'

urlpatterns = [
    url(r'^$', views.accueil, name='accueil'),
    url(r'^liste/$', views.ListeProduit.as_view(), name='liste_produit'),
    url(r'^produit/(?P<pk>\d+)$', views.DetailProduit.as_view(), name='details'),
    url(r'^categorie/(?P<id>\d+)$', views.ListeProduitSousCategorie.as_view(), name='categorie_produit'),
    
]