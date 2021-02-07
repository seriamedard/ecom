from boutique.models import Categorie, SousCategorie, Panier, CompteUser
from boutique.forms import NewsletterForm, ParagraphErrorList
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required


# Exceptions
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist

def get_variable(request):
    devise = "FCFA"
    try:
        liste_categories = Categorie.objects.all()
        liste_sous_categories = SousCategorie.objects.all().order_by('nom')
    except ObjectDoesNotExist:
        liste_categories = []
        liste_sous_categories = []

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
        except UnboundLocalError:
            quantite_dans_panier = 0
            panier = []
            prix_total = 0
        except ObjectDoesNotExist:
            panierproduit = []
            panier = []

        if panier:
            panier = panier.last()
            panierproduit = panier.produits.all()
            quantite_dans_panier = panier.quantite
            prix_total = panier.prix   
        else:
            quantite_dans_panier = 0
            prix_total = 0
            panierproduit = []
    else:
        quantite_dans_panier = 0
        prix_total = 0
        panierproduit = []
        panier = []

    return {
        'quantite_dans_panier':quantite_dans_panier,
        'prix_total':prix_total,
        'panierproduit':panierproduit,
        'panier':panier,
        }