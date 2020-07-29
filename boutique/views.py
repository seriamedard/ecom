from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.urls import reverse, NoReverseMatch, resolve, Resolver404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.debug import sensitive_variables
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q
from datetime import datetime

#exception
from django.core.exceptions import MultipleObjectsReturned

#Import de model
from .models import (Categorie, Produit, SousCategorie,
                    CompteUser, Contact, Panier, Bug, 
                    AvisDemande, Commande)

#import des formulaires
from .forms import (CompteUserForm, ConnexionForm, NewsletterForm, 
                    ParagraphErrorList, PasswordChangeForm, ProfilForm,
                    BugForm, ContactUsForm, PayementForm)

# Views

# Stock dans la boutique avec pagination
def Boutique(request):
    template_name = 'boutique/tous_produits.html'
    liste_produits = Produit.objects.filter(disponible=True).order_by('-date_de_creation')
    paginator = Paginator(liste_produits, 6, orphans=3)
    page = request.GET.get('page')

    try:
        liste_produits = paginator.page(page)
    except PageNotAnInteger:
        liste_produits = paginator.page(1)
    except EmptyPage:
        liste_produits = paginator.page(paginator.num_pages)
    resultat = len(liste_produits)
    return render(request,template_name, locals())


# liste des produits dans chaque sous categorie
def produit_du_sous_categorie(request, id_sous_categorie):

    try:
        id = id_sous_categorie
        liste_produits = get_object_or_404(SousCategorie, pk=id).produit_set.all().order_by('-date_de_creation')
    except ValueError:
        return Http404
    except:
        return Http404

    paginator = Paginator(liste_produits, 6, orphans=2)
    page = request.GET.get('page')
    try:
        liste_produits = paginator.page(page)
    except PageNotAnInteger:
        liste_produits = paginator.page(1)
    except EmptyPage:
        liste_produits = paginator.page(paginator.num_pages)

    return render(request, 'boutique/produit_sous_categorie.html', locals())


#Liste produits dans chaque categorie croisé avec sous categorie
def produit_dans_categorie(request, id_categorie, id_sous_categorie):

    try:
        id_categorie = id_categorie
        id_sous_categorie = id_sous_categorie

        #requete Q(pour chaque categorie et sous categorie on obtient la liste des produits)
        liste_produits = Produit.objects.filter(
            Q(categorie=get_object_or_404(Categorie, id=id_categorie)) & 
            Q(sous_categorie=get_object_or_404(SousCategorie, id=id_sous_categorie))
            ).order_by('-date_de_creation')

    except ValueError:
        return Http404

    paginator = Paginator(liste_produits, 6, orphans=3)
    page = request.GET.get('page')

    try:
        liste_produits = paginator.page(page)
    except PageNotAnInteger:
        liste_produits = paginator.page(1)
    except EmptyPage:
        liste_produits = paginator.page(paginator.num_pages)
    resultat = len(liste_produits)
    return render(request, 'boutique/produit_categorie.html', locals())


# Detail du prduit
class DetailProduit(DetailView):
    model = Produit
    context_object_name = 'un_produit'
    template_name = 'boutique/detail.html'
    
    def get_object(self):
        un_produit = super(DetailProduit, self).get_object()
        un_produit.etoile +=1
        un_produit.save()

        return un_produit


#Accueil
@sensitive_variables('email', 'contact')
def accueil(request):
    """
    liste des 12 produits les plus recents
    """
    liste_produits = Produit.objects.filter(
        disponible=True).order_by('-date_de_creation')[:12]
    liste_produits_promo = Produit.objects.filter(
        disponible=True,
        promotion=True).order_by('-date_de_creation')

    if request.method == "POST":
        envoi = False
        form = NewsletterForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            envoi = True
            contact = Contact.objects.filter(email=email)
            if not contact.exists():
                contact = Contact.objects.create(
                    prenom=last_name, 
                    email=email)
                contact.save()
            else:
                contact.first()
            messages.info(request, "Vous êtes maintenant inscrit aux nouvelles de soma électronic")
        else:
            errors = form.errors.items()
            messages.warning(request, "Une erreur est arrivée, veillez récommencer!")
    else:
        form = NewsletterForm()
    resultat = len(liste_produits)      
    return render(request, 'boutique/index.html', locals())


# Traitement de recherche
def recherche(request):
    query = request.GET.get('query')
    if not query:
        messages.info(request, "Veillez écrire le nom d'un produit pour la recherche.")
        liste_produits = Produit.objects.all()
    else:
        liste_produits = Produit.objects.filter(nom__icontains=query)
    if not liste_produits.exists():
        liste_produits = Produit.objects.filter(sous_categorie__nom__icontains=query)
    if not liste_produits.exists():
        liste_produits = Produit.objects.filter(categorie__nom__icontains=query)
    
    resultat = len(liste_produits)
    return render(request, 'boutique/recherche.html', locals())


# traitement d'inscription
@sensitive_variables('username','email','password','user','profil')
def inscription(request):
    form = CompteUserForm(request.POST or None, error_class=ParagraphErrorList)
    
    if form.is_valid():
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        envoi = True
        user = User.objects.create_user(username=username, 
                            email=email, 
                            password=password,
                            )
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profil = CompteUser(user=user)
        profil.save()
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            messages.add_message(request, messages.INFO, "Vous êtes connecté!")
            return redirect('boutique:profil')
    
    return render(request, 'boutique/inscription.html', locals())


# La connexion
@sensitive_variables('username', 'password', 'user')
def connexion(request):
    
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST, error_class=ParagraphErrorList)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) 
            if user:
                login(request, user)
                return redirect('boutique:accueil')
            else:
                error = True
    else:
        form = ConnexionForm()
        
    return render(request, 'boutique/connexion.html', locals())


# La deconnexion
@sensitive_post_parameters('user','password')
def deconnexion(request):
    logout(request)
    messages.success(request, "vous êtes déconnecté avec succès")
    return redirect("boutique:accueil")

# Gestion du profil
@login_required(login_url='boutique:connexion')
def profil(request):
    profil = get_object_or_404(CompteUser, user=request.user)
    try:
        liste_panier = Panier.objects.filter(user=CompteUser.objects.get(user=request.user),traite=True)
    except:
        liste_panier = []
    return render(request, 'boutique/profil.html', locals())


@login_required(login_url='boutique:connexion')
def modif_profil(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, error_class=ParagraphErrorList)
        user = request.user 
        profil_user =get_object_or_404(CompteUser, user=user)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            bio = form.cleaned_data['bio']
            newsletter = form.cleaned_data['newsletter']

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            profil_user.bio = bio
            profil_user.inscrit_newsletter = newsletter
            profil_user.save()

            if profil_user.inscrit_newsletter:
                contact = Contact.objects.filter(email=email)
                messages.info(request, "Vous êtes maintenant inscrit aux nouvelles de soma électronic")
                if not contact.exists():
                    contact = Contact.objects.create(
                        prenom=last_name, 
                        email=email)
                    contact.save()
                else:
                    contact.first()
            else:
                contact = Contact.objects.filter(email=email)
                if not contact.exists():
                    pass
                else:
                    contact.first().delete()
                    profil_user.save()
            return redirect('boutique:profil')
    else:
        form = form = ProfilForm()
    
    return render(request, 'boutique/modif_profil.html', locals())

# Changer le mot de passe
@login_required(login_url='boutique:connexion')
def changer_mot_de_passe(request):
    error = False
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, error_class=ParagraphErrorList)
        user = request.user
       
        if form.is_valid():
            oldpassword = form.cleaned_data['oldpassword']
            newpassword = form.cleaned_data['newpassword']
            if user.check_password(oldpassword):
                user.set_password(newpassword)
                user.save()
                messages.success(request, "Mot de passe modifier avec succès!")
                return redirect('boutique:profil')
            else:
                error = True
    else:
        form = PasswordChangeForm(request.POST or None)
    
    return render(request, 'boutique/changemdp.html', locals())


# Traitement du panier
@login_required(login_url='boutique:connexion')
def ajout_au_panier(request):
    """
    -si user a un panier encours, on recupere le panier et on continue les transactions,
    -sinon on crée un panier et on fait la transaction, au suivante transaction on itere la premier,
    -si un produit n'est pas dans le panier , on l'ajout en faisant des calculs sur le panier,
    -sinon on prend le premier produit et et on met à jour les données des transactions sur ce produit,
    """
    quantite = 0
    if request.method == 'GET':
        panier = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
        if not panier.exists():
            panier = Panier.objects.create(user=CompteUser.objects.get(user=request.user))
            panier.nom_du_panier()
        else:
            panier = panier.last()

        try:
            id=int(request.GET.get('ajout-panier'))
            produit = Produit.objects.get(id=id)
            produit_panier = panier.produits.filter(id=produit.id)
        except:
            return Http404

        quatite_un_produit = 0 #initialisation
        if produit_panier:
            quatite_un_produit += 1
            produit_panier = produit_panier.first()
            quantite += 1
            panier.quantite += quantite
            prix_produit = produit_panier.prix * quatite_un_produit
            panier.prix += prix_produit
            panier.save()
        else:
            panier.produits.add(produit)
            messages.success(request, "Produit ajouté au panier!")
            quatite_un_produit = 1
            quantite = 1
            prix_produit = produit.prix * quatite_un_produit
            panier.quantite += quantite
            panier.prix += prix_produit
            panier.save()

    try:
        panierproduit = Panier.objects.get(user=CompteUser.objects.get(user=request.user), traite=False).produits.all()
    except MultipleObjectsReturned:
        panierproduit = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
        panierproduit = panierproduit.last().produits.all()
    except :
        panierproduit = []

    return render(request, 'boutique/panier.html', locals())

@login_required(login_url='boutique:connexion')
def sup_item_panier(request, id_produit): #bug
    try:
        id=int(id_produit)
        paniersup = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
    except ValueError:
        return Http404
    if not paniersup.exists():
        raise Http404
    else:
        paniersup = paniersup.last()
        paniersup.produits.get(id=id).clear()
        paniersup.save()
        # if lenprod ==0:
        #     return redirect('boutique:boutique')
    return render(request, 'boutique/panier.html', locals())



def acheter(request, id_produit): #bug
    if request.user.is_authenticated:
        profil = CompteUser.objects.get(user=request.user)
        panier = Panier.objects.filter(user=profil, traite=False)
        if not panier.exists():
            produit = get_object_or_404(Produit,id=id_produit)
        else:
            produit = get_object_or_404(Produit,id=id_produit)
            panier= panier.last()
            panier.produits.add(produit)
            panier.save()
    else:
        produit = get_object_or_404(Produit,id=id_produit)
        quantite_produit = 1
        prix_produit = quantite_produit * produit.prix

    formu = PayementForm(request.POST or None)
    envoi = False
    if formu.is_valid():
        nom = formu.cleaned_data['nom']
        prenom = formu.cleaned_data['prenom']
        email = formu.cleaned_data['email']
        adress = formu.cleaned_data['adress']
        telephone = formu.cleaned_data['telephone']
        newsletter = formu.cleaned_data['newsletter']

        envoi = True #envoi de mail
        #enregistrement du contact
        contact = Contact.objects.filter(email=email)
        if contact.exists(): 
            contact=contact.first()
            contact.nom = nom
            contact.prenom = prenom
            contact.adress = adress
            contact.numero_de_telephone = telephone
            contact.save()
        else:
            contact = Contact.objects.create(prenom=prenom, numero_de_telephone=telephone, email=email, adress=adress)
            contact.save()
        
        #enregistrement de la commande

        if produit:
            produit.quantite -=1
            produit.save()

        if request.user.is_authenticated:
            if panier:
                panier.traite = True
                panier.save()
                commande = Commande.objects.create(contact=contact, panier=panier)
                commande.save()
            else:
                commande = Commande.objects.create(contact=contact, produit=produit)
                commande.save() 
        else:
            commande = Commande.objects.create(contact=contact, produit=produit)
            commande.save()

        return redirect('boutique:merci')
    return render(request, 'boutique/achat.html', locals()) 

@login_required()
def lacaisse(request):
    profil = CompteUser.objects.get(user=request.user)
    panier = Panier.objects.filter(user=profil, traite=False)
    panier = panier.last()

    formu = PayementForm(request.POST or None)
    envoi = False
    if formu.is_valid():
        nom = formu.cleaned_data['nom']
        prenom = formu.cleaned_data['prenom']
        email = formu.cleaned_data['email']
        adress = formu.cleaned_data['adress']
        telephone = formu.cleaned_data['telephone']
        newsletter = formu.cleaned_data['newsletter']

        envoi = True #envoi de mail
        #enregistrement du contact
        contact = Contact.objects.filter(email=email)
        if contact.exists(): 
            contact=contact.first()
            contact.nom = nom
            contact.prenom = prenom
            contact.adress = adress
            contact.numero_de_telephone = telephone
            contact.save()
        else:
            contact = Contact.objects.create(prenom=prenom, numero_de_telephone=telephone, email=email, adress=adress)
            contact.save()

        panier.traite = True
        panier.save()
        commande = Commande.objects.create(contact=contact, panier=panier)
        commande.save()
        return redirect('boutique:merci')
    return render(request, 'boutique/caisse.html', locals())

def signal_bug(request):
    form = BugForm(request.POST or None)
    envoi = False
    if form.is_valid():
        description = form.cleaned_data['description']
        bug = Bug.objects.create(description=description)
        bug.save()
        envoi = True
        messages.success(request, "Votre demande a été enregistée. Merci!")
        return redirect('boutique:accueil')
    return render (request,'boutique/bug.html', locals())

def contacter(request):
    form = ContactUsForm(request.POST or None)
    if form.is_valid():
        prenom = form.cleaned_data['prenom']
        email = form.cleaned_data['email']
        demande = form.cleaned_data['demande']
        newsletter = form.cleaned_data['newsletter']

        un_avis = AvisDemande.objects.create(prenom=prenom,
                                            email=email,
                                            demande=demande)
        un_avis.save()
        messages.success(request, "Merci de nous avoir écrit. Nous allons vous répondre sous peu.")
        envoie = True #envoie de mail
        if newsletter == True:
            contact= Contact.objects.filter(email=email)
            if contact.exists():
                contact = contact.first().save()
            else:
                contact = Contact.objects.create(prenom=prenom, email=email)
                contact.save()

        return redirect('boutique:accueil')
    return render(request, 'boutique/contacter.html', locals())

   
    
