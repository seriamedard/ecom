from django.conf.urls import url
from . import views


app_name = 'boutique'

urlpatterns = [
    url(r'^$', views.accueil, name='accueil'),
    url(r'^liste/$', views.ListeProduit.as_view(), name='liste_produit'),
    url(r'^boutique$', views.Boutique, name='boutique'),
    url(r'^produit/(?P<pk>\d+)$', views.DetailProduit.as_view(), name='details'),
    url(r'^categorie/(?P<id>\d+)$', views.ListeProduitSousCategorie.as_view(), name='categorie_produit'),
    url(r'^souscategorie/(?P<id_sous_categorie>\d+)$', views.produit_du_sous_categorie, name='sous_categorie_produit'),
    url(r'^categorie/(?P<id_categorie>\d+)/(?P<id_sous_categorie>\d+)$',views.produit_dans_categorie, name="categorie_liste_produit"),
    
]