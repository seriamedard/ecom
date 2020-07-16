from django.contrib import admin

from .models import Produit, SousCategorie, Categorie
# Register your models here.

class SousCategorieInline(admin.TabularInline):
    """
    model = Produit
    fieldsets = [
        (None, {'fields':['sous_categorie', 'categorie']})
    ]
    verbose_name = "Sous Catégorie"
    verbose_name_plural = "Sous Catégories"
    """
    pass


@admin.register(SousCategorie)
class SousCategorieAdmin(admin.ModelAdmin):
    pass


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    #inlines = [SousCategorieInline,]
    fields = (
        'nom', 
        'description', 
        'quantite', 
        'disponible', 
        'promotion',
        'etoile',
        'premier_prix',
        'prix',
        'taux_reduction',
        'slug',
        'image',
        'sous_categorie',
        'categorie' 
        )
    search_fields = ('nom', 'sous_categorie')
    prepopulated_fields = {"slug": ("nom",)}

    def reduction(self, produit):
        self.taux = 1 - (produit.prix / produit.premier_prix)
        produit.taux_reduction = self.taux
        return produit.taux_reduction
    




class CategorieSousCategorieInline(admin.TabularInline):
    model = Categorie.souscategorie.through


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [CategorieSousCategorieInline]