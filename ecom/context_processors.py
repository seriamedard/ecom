from boutique.models import Categorie, SousCategorie

def get_variable(request):
    devise = "FCFA"
    liste_categories = Categorie.objects.all()
    liste_sous_categories = SousCategorie.objects.all().order_by('nom')
    
    return {
        'devise':devise,
        'liste_categories':liste_categories,
        'liste_sous_categories':liste_sous_categories,
        }