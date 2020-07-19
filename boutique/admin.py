from django.contrib import admin 
from django.forms import ModelForm

from .models import Produit, SousCategorie, Categorie
# Register your models here.

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
        nom = cleaned_data.get('nom')
        description = cleaned_data.get('description')
        quantite =  cleaned_data.get('quantite')
        disponible = cleaned_data.get('disponible')
        promotion = cleaned_data.get('promotion')
        etoile = cleaned_data.get('etoile')
        premier_prix = cleaned_data.get('premier_prix')
        prix = cleaned_data.get('prix')
        taux_reduction = cleaned_data.get('taux_reduction')
        image = cleaned_data.get('image')
        sous_categorie = cleaned_data.get('sous_categorie')
        categorie = cleaned_data.get('categorie')
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
    #inlines = [SousCategorieInline,]

    form = ProduitAdminForm
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
        'categorie', 
        'date_de_creation',
        )
    list_filter = ('promotion','prix')
    list_display = ['nom','disponible','promotion','prix']
    search_fields = ('nom', 'sous_categorie')
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

    # def get_form(self, request, obj=Produit, **kwargs):
    #     form = super(ProduitAdmin, self).get_form(request,obj=produit, **kwargs)
    #     form.base_fields['taux_reduction'].initial = (1 - obj.prix / obj.premier_prix)*100
    #     return form
    



    




class CategorieSousCategorieInline(admin.TabularInline):
    model = Categorie.souscategorie.through


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [CategorieSousCategorieInline]
    filter_horizontal = ('souscategorie',)