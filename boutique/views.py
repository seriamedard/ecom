from django.shortcuts import render, get_object_or_404, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Categorie, Produit, SousCategorie


# Views

# Stock dans la boutique avec pagination
def Boutique(request):
    template_name = 'boutique/tous_produits.html'
    liste_produits = Produit.objects.filter(disponible=True).order_by('-date_de_creation')
    paginator = Paginator(liste_produits, 6, orphans=3)
    page = request.GET.get('page')

    try:
        liste_produits = paginator.page(page)
    except PageNotAnInteger:
        liste_produits = paginator.page(1)
    except EmptyPage:
        liste_produits = paginator.page(paginator.num_pages)

    return render(request,template_name, locals())


# liste des produits dans chaque sous categorie
def produit_du_sous_categorie(request, id_sous_categorie):

    try:
        id = id_sous_categorie
        liste_produits = get_object_or_404(SousCategorie, pk=id).produit_set.all().order_by('-date_de_creation')
    except ValueError:
        return Http404
    except:
        return Http404

    paginator = Paginator(liste_produits, 6, orphans=2)
    page = request.GET.get('page')
    try:
        liste_produits = paginator.page(page)
    except PageNotAnInteger:
        liste_produits = paginator.page(1)
    except EmptyPage:
        liste_produits = paginator.page(paginator.num_pages)

    return render(request, 'boutique/produit_sous_categorie.html', locals())


#Liste produits dans chaque categorie croisé avec sous categorie
def produit_dans_categorie(request, id_categorie, id_sous_categorie):

    try:
        id_categorie = id_categorie
        id_sous_categorie = id_sous_categorie

        #requete Q(pour chaque categorie et sous categorie on obtient la liste des produits)
        liste_produits = Produit.objects.filter(
            Q(categorie=get_object_or_404(Categorie, id=id_categorie)) & 
            Q(sous_categorie=get_object_or_404(SousCategorie, id=id_sous_categorie))
            ).order_by('-date_de_creation')

    except ValueError:
        return Http404

    paginator = Paginator(liste_produits, 6, orphans=3)
    page = request.GET.get('page')

    try:
        liste_produits = paginator.page(page)
    except PageNotAnInteger:
        liste_produits = paginator.page(1)
    except EmptyPage:
        liste_produits = paginator.page(paginator.num_pages)

    return render(request, 'boutique/produit_categorie.html', locals())


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
    liste des 12 produits les plus recents
    """
    liste_produits = Produit.objects.filter(
        disponible=True).order_by('-date_de_creation')[:12]
    liste_produits_promo = Produit.objects.filter(
        disponible=True,
        promotion=True).order_by('-date_de_creation')

    return render(request, 'boutique/index.html', locals())


# Traitement de recherche
def recherche(request):
    query = request.GET.get('query')
    if not query:
        liste_produits = Produit.objects.all()
    else:
        liste_produits = Produit.objects.filter(nom__icontains=query)
    if not liste_produits.exists():
        liste_produits = Produit.objects.filter(sous_categorie__nom__icontains=query)
    if not liste_produits.exists():
        liste_produits = Produit.objects.filter(categorie__nom__icontains=query)
    
    resultat = len(liste_produits)
    
    return render(request, 'boutique/recherche.html', locals())


def newsletter(request):
    return render(request, 'boutique/newsletter.html', locals())






   
    
