from boutique.models import Categorie, SousCategorie, Panier, CompteUser
from boutique.forms import NewsletterForm, ParagraphErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist

def get_variable(request):
    devise = "FCFA"
    liste_categories = Categorie.objects.all()
    liste_sous_categories = SousCategorie.objects.all().order_by('nom')
    form = NewsletterForm()

    return {
        'devise':devise,
        'liste_categories':liste_categories,
        'liste_sous_categories':liste_sous_categories,
        'form':form,
        }

def get_variable_panier(request):
    if request.user.is_authenticated:
        try:
            panier = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
            panierproduit = Panier.objects.get(user=CompteUser.objects.get(user=request.user), traite=False).produits.all()
        except UnboundLocalError:
            quantite_dans_panier = 0
        except MultipleObjectsReturned:
            panierproduit = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
            panierproduit = panierproduit.last().produits.all()
        except ObjectDoesNotExist:
            panierproduit = []
        if panier:
            panier = panier.last()
            quantite_dans_panier = panier.quantite
            prix_total = panier.prix
        else:
            quantite_dans_panier = 0
            prix_total = 0
    else:
        quantite_dans_panier = 0
        prix_total = 0
        panierproduit = []
    
        # quantite_dans_panier = 0
        # prix_total = 0
    return {
        'quantite_dans_panier':quantite_dans_panier,
        'prix_total':prix_total,
        'panierproduit':panierproduit,
        }