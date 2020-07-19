from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
# Create your models here.


class SousCategorie(models.Model):
    nom = models.CharField(max_length=100)
    date_de_creation = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'sous categorie'
        verbose_name_plural = 'sous categories'
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    date_de_creation = models.DateField(auto_now_add=True)
    souscategorie = models.ManyToManyField(
        SousCategorie, 
        blank=True
    )

    class Meta:
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    disponible = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='images/', 
        default='images/photo.jpg'
        )
    quantite = models.IntegerField('quantité', default=1)
    premier_prix = models.FloatField(default=0.0, max_length=None)
    prix = models.FloatField(default=0.0)
    taux_reduction = models.FloatField('taux de réduction',blank=True, default=0, max_length=3)
    promotion = models.BooleanField('Mise en promotion', default=False)
    etoile = models.IntegerField('Nombre de vue', default=0)
    date_de_creation = models.DateField('Ajouter le', auto_now_add=True)
    slug = models.SlugField(max_length=150, null=True)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        null=True
        )

    sous_categorie = models.ForeignKey(
        SousCategorie, 
        on_delete=models.CASCADE, 
        verbose_name="Les sous categories"
        )

    class Meta:
        verbose_name = 'produit'
        verbose_name_plural = 'produits'
        ordering = ['-date_de_creation']

    def __str__(self):
        return self.nom

    def reduction(self, *args, **kwargs):
        self.taux_reduction  = (1 - self.prix / self.premier_prix)*100
        return self.taux_reduction


@receiver(post_delete, sender=Produit)
def produit_suppression(sender, instance, **kwargs):
    print('un produit vient d''être supprimer')


class CompteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    inscrit_newsletter = models.BooleanField(default=False)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)

class Panier(models.Model):
    nom = models.CharField(max_length=300)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    produits = models.ManyToManyField(Produit, null=True, blank=True)
    








