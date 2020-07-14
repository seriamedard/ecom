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
    prepopulated_fields = {"slug": ("nom",)}



class CategorieSousCategorieInline(admin.TabularInline):
    model = Categorie.souscategorie.through


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [CategorieSousCategorieInline]