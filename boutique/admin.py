from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib import admin 

from .models import (Produit, SousCategorie, Categorie, 
                    CompteUser, Contact, Media, 
                    Panier, Bug, Commande, AvisDemande,
                    PanierItem)

# Register Admin.

class CategorieSousCategorieInline(admin.TabularInline):
   
    model = Categorie.souscategorie.through
    verbose_name = "Sous Catégorie"
    verbose_name_plural = "Sous Catégories"
    extra = 1


@admin.register(SousCategorie)
class SousCategorieAdmin(admin.ModelAdmin):
    inlines = [CategorieSousCategorieInline,]

class ProduitAdminForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        quantite =  cleaned_data.get('quantite')
        premier_prix = cleaned_data.get('premier_prix')
        prix = cleaned_data.get('prix')
        quantite = cleaned_data.get('quantite')

        #quantite
        if quantite < 0:
            msg = "Entrer un entier plus grand que 0"
            self.add_error('quantite', msg)

        #premier prix
        if premier_prix <=0:
            msg = "Le Premier prix d'un produit doit être positif et plus grand que le prix normal"
            self.add_error('premier_prix', msg)
        
        #prix
        if prix <0 :
            msg = "Le prix d'un produit doit être positif"
            self.add_error('prix', msg)
        elif prix > premier_prix :
            msg = "Le prix d'un produit doit être inferieur au premier prix"
            self.add_error('prix', msg)
        elif prix <=0 and prix > premier_prix:
            msg = "Le prix d'un produit doit être positif et inferieur au premier prix"
            self.add_error('prix', msg)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    form = ProduitAdminForm
    fieldsets = (
        ('Titre',{
            'fields':('nom','slug', 'description', 'image','picture', 'date_de_creation')
        }),
        ('Prix-Qté',{
            'classes':('collapse',),
            'fields': ('quantite','disponible','promotion','etoile','premier_prix','prix','taux_reduction')
        }),
        ('Categories',{
            'classes':('collapse',),
            'fields': ('sous_categorie','categorie','media'),
        }),
    )

    list_filter = ('promotion','prix')
    list_display = ['nom','disponible','promotion','prix']
    search_fields = ['nom']
    filter_horizontal = ('media',)
    prepopulated_fields = {
        "slug": ("nom",),
        }
    
    readonly_fields = ('date_de_creation','etoile')
    show_full_result_count = True
    date_hierarchy = 'date_de_creation'
    empty_value_display = 'vide'
    list_per_page = 20
    actions = ['promotion']
    
    def promotion(self,request, queryset):
        queryset.update(taux_reduction=True)
    promotion.short_description = "Mise en Promotion"
    
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [CategorieSousCategorieInline]
    filter_horizontal = ('souscategorie',)


@admin.register(CompteUser)
class CompteUserAdmin(admin.ModelAdmin):
    list_display = ['user']
    readonly_fields = ['user','bio', 'inscrit_newsletter']
    empty_value_display = 'vide'
    list_per_page = 20


@admin.register(Contact)
class ContactForm(admin.ModelAdmin):
    readonly_fields = ['prenom', 'email']
    list_display = ['email', 'prenom','numero_de_telephone']
    empty_value_display = 'Vide'
    list_per_page = 10

admin.site.register(Media)

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    readonly_fields = ['nom', 'produits', 'user', 'quantite', 'prix']
    filter_horizontal = ('produits',)
    list_display = ['nom','traite','terminer']
    list_filter = ['terminer']


@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    readonly_fields = ['description']
    list_display = ['__str__','date']

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    readonly_fields = ['nom','date','contact']
    list_display = ['nom','date','valider']

@admin.register(AvisDemande)
class AvisDemandeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'email']
    readonly_fields = ['date', 'prenom', 'demande']


admin.site.register(PanierItem)