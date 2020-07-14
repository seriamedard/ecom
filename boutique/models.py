from django.db import models

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
    quantite = models.IntegerField(default=1)
    premier_prix = models.FloatField(default=0.0)
    prix = models.FloatField()
    taux_reduction = models.FloatField(blank=True, default=0)
    promotion = models.BooleanField(default=False)
    etoile = models.IntegerField(default=0)
    date_de_creation = models.DateField(auto_now_add=True)
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





