from django.shortcuts import render
from django.views.generic import ListView, DetailView

# import de tous les models
from .models import Categorie, Produit, SousCategorie

"""
Le traitement des vues
"""

# Listes des produits
class ListeProduit(ListView):
    model = Produit
    context_object_name = 'liste_produits'
    template_name = 'boutique/liste.html'
    queryset = Produit.objects.filter(disponible=True).order_by('-date_de_creation')
    devise = "FCFA"
    def get_context_data(self, **kwargs):
        context = super(ListeProduit, self).get_context_data(**kwargs)
        context['devise'] = self.devise


# Promotion
class Promo(ListeProduit):
    template_name = 'boutique/promo.html'
    def get_queryset(self):
        return Produit.objects.filter(disponible=True, promotion=True).order_by('-date_de_creation')

class ListeCategorie(ListView):
    model = Categorie
    context_object_name = 'liste_categories'
    template_name = 'boutique/categorie.html'


# lites des produits d'un sous categorie
class ListeProduitSousCategorie(ListView):
    model = Produit
    context_object_name = 'liste_produits' #produit du sous categorie
    template_name = 'boutique/sous_produit.html'

    def get_queryset(self):
        return Produit.objects.filter(
            disponible=True, 
            sous_categorie__id=self.kwargs['id']).order_by('-date_de_creation')

    def get_context_data(self, **kwargs):
        context = super(ListeProduitSousCategorie, self).get_context_data(**kwargs)
        context['liste_sous_categories'] = SousCategorie.objects.all()
        return context


# Detail du prduit
class DetailProduit(DetailView):
    model = Produit
    context_object_name = 'un_produit'
    template_name = 'boutique/detail.html'
    
    def get_object(self):
        un_produit = super(DetailProduit, self).get_object()
        un_produit.etoile +=1
        un_produit.save()
        return un_produit


#Accueil
def accueil(request):
    """
    liste des 15 produits les plus recents
    """
    liste_produits = Produit.objects.filter(disponible=True).order_by('-date_de_creation')[:20]
    liste_categories = Categorie.objects.all()
    liste_sous_categories = SousCategorie.objects.all().order_by('nom')
    return render(request, 'boutique/index.html', locals())

#Vue recherche
def recherche(request):
    pass

# Vue ajout au panier
def ajout_panier(request):
    pass





   
    
