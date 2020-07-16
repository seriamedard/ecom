from django.shortcuts import render, get_object_or_404, Http404
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

    """
    La pagination est requise ici
    """
    def get_context_data(self, **kwargs):
        context = super(ListeProduit, self).get_context_data(**kwargs)
        context['devise'] = self.devise

#stock boutique avec pagination
def Boutique(request):
    template_name = 'boutique/tous_produits.html'
    liste_produits = Produit.objects.filter(disponible=True).order_by('-date_de_creation')
    liste_categories = Categorie.objects.all()
    liste_sous_categories = SousCategorie.objects.all().order_by('nom')
    devise = "FCFA"

    """
    La pagination est requise ici
    """
    return render(request,template_name, locals())


# Listes des categories
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


# liste des produits dans chaque sous categorie
def produit_du_sous_categorie(request, id_sous_categorie):
    try:
        id = id_sous_categorie
    except:
        return Http404

    liste_produits = SousCategorie.objects.get(id=id).produit_set.all()
    liste_categories = Categorie.objects.all()
    liste_sous_categories = SousCategorie.objects.all().order_by('nom')
    devise = "FCFA"

    """
    La pagination est requise ici
    """
    return render(request, 'boutique/produit_sous_categorie.html', locals())
#Liste produits dans chaque categorie croisé avec sous categorie
def produit_dans_categorie(request, id_categorie, id_sous_categorie):
    try:
        id_categorie = id_categorie
        id_sous_categorie = id_sous_categorie
    except:
        return Http404
    liste_produits =Categorie.objects.get(id=id_categorie).souscategorie.get(id=id_sous_categorie).produit_set.all()
    liste_categories = Categorie.objects.all()
    liste_sous_categories = SousCategorie.objects.all().order_by('nom')
    devise = "FCFA"

    """
    La pagination est requise ici
    """
    return render(request, 'boutique/produit_categorie.html', locals())

# Detail du prduit
class DetailProduit(DetailView):
    model = Produit
    context_object_name = 'un_produit'
    template_name = 'boutique/detail.html'
    devise = "FCFA"
    
    def get_object(self):
        un_produit = super(DetailProduit, self).get_object()
        un_produit.etoile +=1
        un_produit.save()
        return un_produit

    def get_context_data(self, **kwargs):
        context = super(DetailProduit, self).get_context_data(**kwargs)
        context['liste_categories'] = Categorie.objects.all()
        context['liste_sous_categories'] = SousCategorie.objects.all()  
        context['devise'] = self.devise
        return context


#Accueil
def accueil(request):
    """
    liste des 15 produits les plus recents
    """
    liste_produits = Produit.objects.filter(disponible=True).order_by('-date_de_creation')[:12]
    liste_categories = Categorie.objects.all()
    liste_sous_categories = SousCategorie.objects.all().order_by('nom')
    liste_produits_promo = Produit.objects.filter(disponible=True, promotion=True).order_by('-date_de_creation')
    devise = "FCFA"
    return render(request, 'boutique/index.html', locals())

#Vue recherche
def recherche(request):
    pass






   
    
