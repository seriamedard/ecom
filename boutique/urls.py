from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from . import views
from .forms import ConnexionForm


app_name = 'boutique'

urlpatterns = [
    url(r'^$', views.accueil, name='accueil'),
    url(r'^boutique$', views.Boutique, name='boutique'),
    path('boutique/produit/<int:pk>-<str:slug>/', views.DetailProduit.as_view(), name='details'),
    url(r'^souscategorie/(?P<id_sous_categorie>\d+)$', views.produit_du_sous_categorie, name='sous_categorie_produit'),
    url(r'^categorie/(?P<id_categorie>\d+)/(?P<id_sous_categorie>\d+)$',views.produit_dans_categorie, name="categorie_liste_produit"),
    url(r'^recherche/$', views.recherche, name='recherche'),
    url(r"inscription/", views.inscription, name='inscription'),
    url(r'^connexion/$', views.connexion , name='connexion'),
    url(r'^deconnexion/$', views.deconnexion, name='deconnexion'),
    url(r'^passwordchange/$', views.changer_mot_de_passe, name='passwordchange'),
    url(r'^profil/$', views.profil, name='profil'),
    url(r'^profil/modifprofil/$', views.modif_profil, name='modif_profil'),
    url(r'^produit/achat/(?P<id_produit>\d+)/$', views.acheter, name='achat'),
    url(r'^ajout-au-panier/$', views.ajout_au_panier, name='ajout_au_panier'),
    path('sup-item-paier/<int:pk>/', views.sup_item_panier, name='supprimer'),
    url(r'^commandevalider/$', TemplateView.as_view(template_name='boutique/merci.html'), name="merci"),
    url(r'^Valider/$', TemplateView.as_view(template_name='boutique/aurevoir.html'), name="aurevoir"),
    url(r'^validercaisse/$', views.lacaisse , name='caisse'),
    url(r'^sinalbug/$', views.signal_bug, name='bug'),
    url(r'^contact/$', views.contacter, name="contacter"),
]