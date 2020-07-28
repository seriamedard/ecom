import os
import argparse
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class SousCategorie(models.Model):
    nom = models.CharField(max_length=100)
    date_de_creation = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sous Categorie'
        verbose_name_plural = 'Sous Categories'
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


def renommage(instance, nom_fichier):
    return "{}-{}".format(instance.id, nom_fichier)

class Media(models.Model):
    nom = models.CharField(max_length=100)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, blank=True)
    image = models.FileField(upload_to=renommage, verbose_name='Image plus')

    def save(self, *args, **kwargs):

        if self.id is None:
            saved_image=self.image
            self.image = None
            super(Media, self).save(*args, **kwargs)
            self.image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super(Media, self).save(*args, **kwargs)

    def __str__(self):
        return '{}_{}'.format(self.nom,self.image.name)


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
    media = models.ManyToManyField(Media, blank=True)

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
    bio = models.TextField(blank=True, null=True)
    inscrit_newsletter = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    def __str__(self):
        return "Profil de {0}".format(self.user.username)


class Panier(models.Model):
    nom = models.CharField(max_length=300, blank=True)
    date_de_creation = models.DateTimeField('Date de création', auto_now_add=True)
    produits = models.ManyToManyField(Produit, blank=True, related_name='produits')
    user = models.ForeignKey(CompteUser, related_name='utilisateur', on_delete=models.CASCADE, blank=True, null=True)
    quantite = models.PositiveIntegerField('Quantité', default=0)
    prix = models.PositiveIntegerField('Prix',default=0)
    traite = models.BooleanField('Traité',default=False)
    terminer = models.BooleanField('Terminé', default=False)

    def nom_du_panier(self):
        self.nom = "Panier du {} par {}".format(datetime.now(), self.user.user.username)
        return self.nom

    def __str__(self):
        return self.nom
    

    
class Contact(models.Model):
    prenom = models.CharField(max_length=100)
    numero_de_telephone = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return "{} : contact {}".format(self.prenom, self.id)

class Bug(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    corrige = models.BooleanField(default=False)
    description = models.TextField()

    class Meta:
        verbose_name = "Rapport de bug"
        verbose_name_plural = "Rapports de bug"
    
    def __str__(self):
        return "{}...".format(self.description[:15])














