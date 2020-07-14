from django.shortcuts import render
from django.views.generic import ListView, DetailView

#import de tous les models
from .models import Categorie, Produit, SousCategorie

"""
Le traitement des vues
"""

#Listes des produits
class ListeProduit(ListView):
    model = Produit
    context_object_name = 'produits'
    template_name = 'boutique/liste.html'
    queryset = Produit.objects.filter(disponible=True).order_by('-date_de_creation')



#lites des produits d'un sous categorie
class ListeProduitSousCategorie(ListView):
    model = Produit
    context_object_name = 'sous_produits' #produit du sous categorie
    template_name = 'boutique/sous_produit.html'

    def get_queryset(self):
        return Produit.objects.filter(
            disponible=True, 
            sous_categorie__id=self.kwargs['id']).order_by('-date_de_creation')

    def get_context_data(self, **kwargs):
        context = super(ListeProduitSousCategorie, self).get_context_data(**kwargs)
        context['sous_categories'] = SousCategorie.objects.all()
        return context


#Detail du prduit
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
    produits_recents = Produit.objects.filter(disponible=True).order_by('-date_de_creation')[:20]
    categories_liste = Categorie.objects.all()
    sous_categorie = SousCategorie.objects.all().order_by('nom') 
    promo_liste = Produit.objects.filter(disponible=True, promotion=True)
    #souscategorie = Categorie.objects.get(nom=cat).souscategorie_set.all()
    return render(request, 'boutique/index.html', locals())

#Vue recherche
def recherche(request):
    pass

# Vue ajout au panier
def ajout_panier(request):
    pass





   
    
