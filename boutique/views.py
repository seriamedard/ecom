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
from django.db import transaction, IntegrityError
from datetime import datetime

# exception
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

# Import de model
from .models import (Categorie, Produit, SousCategorie,
                    CompteUser, Contact, Panier, Bug, 
                    AvisDemande, Commande, PanierItem)

# import des formulaires
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

# Liste produits dans chaque categorie croisé avec sous categorie
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

# Accueil
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
            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        contact = Contact.objects.create(
                            prenom=last_name, 
                            email=email)
                        contact.save()
                    else:
                        contact.first()
                    messages.info(request, "Vous êtes maintenant inscrit aux nouvelles de soma électronic")
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de récommencer."
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
    try:
        if not query:
            messages.info(request, "Veillez écrire le nom d'un produit pour la recherche.")
            liste_produits = Produit.objects.all()
        else:
            liste_produits = Produit.objects.filter(nom__icontains=query)
        if not liste_produits.exists():
            liste_produits = Produit.objects.filter(sous_categorie__nom__icontains=query)
        if not liste_produits.exists():
            liste_produits = Produit.objects.filter(categorie__nom__icontains=query)
    except IntegrityError:
        liste_produits = []

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
        try:
            with transaction.atomic():
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
                    return redirect('boutique:accueil')
        except IntegrityError:
            messages.warning(request, "Une erreur est arrivée, veillez récommencer!")
            return redirect('boutique:accueil')
    
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
                redirection = request.GET.get('next')

                if redirection:
                    return redirect(redirection)
                else:
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
    messages.success(request, "vous êtes maintenant déconnecté !")
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

# Modification du compte
@login_required(login_url='boutique:connexion')
def modif_profil(request):
    form = ProfilForm(request.POST, error_class=ParagraphErrorList)
    if request.method == 'POST':
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
                try:
                    with transaction.atomic():
                        contact = Contact.objects.filter(email=email)
                        messages.info(request, "Vous êtes maintenant inscrit aux nouvelles de soma électronic")
                        if not contact.exists():
                            contact = Contact.objects.create(
                                prenom=last_name, 
                                email=email)
                            contact.save()
                        else:
                            contact.first()
                except IntegrityError:
                    form.errors['internal'] = 'Une erreur interne est apparue. Merci de récommencer'
            else:
                try:
                    with transaction.atomic():
                        contact = Contact.objects.filter(email=email)
                        if not contact.exists():
                            pass
                        else:
                            contact.first().delete()
                            profil_user.save()
                except IntegrityError:
                    form.errors['internal'] = 'Une erreur interne est apparue. Merci de récommencer'
            return redirect('boutique:profil')
    
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
            try:
                with transaction.atomic():
                    if user.check_password(oldpassword):
                        user.set_password(newpassword)
                        user.save()
                        messages.success(request, "Mot de passe modifier avec succès!")
                        return redirect('boutique:profil')
                    else:
                        error = True
            except IntegrityError:
                form.errors['internal'] = 'Une erreur interne est apparue. Merci de récommencer'

    else:
        form = PasswordChangeForm(request.POST or None)
    
    return render(request, 'boutique/changemdp.html', locals())

# Traitement du panier
@login_required(login_url='boutique:connexion')
def ajout_au_panier(request):
    """
    -si user a un panier encours, on recupere le panier et on continue les transactions,
    -sinon on crée un panier et on fait la transaction, au suivante transaction on itere le premier,
    -si un produit n'est pas dans le panier , on l'ajoute en faisant des calculs sur le panier,
    -sinon on prend le premier produit et et on met à jour les données des transactions sur ce produit,
    """
    if request.method == 'GET':
        try:
            with transaction.atomic():
                panier = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
                if not panier.exists():
                    panier = Panier.objects.create(user=CompteUser.objects.get(user=request.user))
                    panier.nom_du_panier()
                    panier.save()
                else:
                    panier = panier.last()

                try:
                    id=int(request.GET.get('ajout-panier'))
                    produit = Produit.objects.get(id=id)
                    panierinter = panier.produits.filter(produits=produit, user=CompteUser.objects.get(user=request.user))
                except:
                    return Http404
                    # pass

                #initialisation
                if panierinter: #s'il y'a deja le produit dans le panier
                    panierinter = panierinter.first()
                    panier.prix -= panierinter.prix_du_produit
                    panier.quantite -= panierinter.quantite_du_produit
                    panier.save()
                    panierinter.quantite_du_produit += 1
                    panierinter.save()
                    panierinter.prix_du_produit = panierinter.quantite_du_produit * panierinter.produits.prix
                    panierinter.save()
                    panier.prix += panierinter.prix_du_produit
                    panier.quantite += panierinter.quantite_du_produit
                    panier.save()
                    messages.success(request, "Produit {} a été mise à jour dans le panier !".format(Produit.objects.get(id=id).nom))

                else:
                    panierinter = PanierItem.objects.create(produits=produit, user=CompteUser.objects.get(user=request.user))
                    panier.produits.add(panierinter)
                    panierinter.save()
                    panier.save()
                    panierinter.quantite_du_produit = 1
                    panierinter.save()
                    panierinter.prix_du_produit = panierinter.quantite_du_produit * panierinter.produits.prix
                    panierinter.save()
                    panier.prix += panierinter.prix_du_produit
                    panier.quantite += panierinter.quantite_du_produit
                    panier.save()
                    messages.success(request, "Produit ajouté au panier!")
        except IntegrityError:
            messages.warning(request, "Une erreur est apparue en interne. Merci de récommencer")
            return redirect('boutique:accueil')

    if request.method == "POST":
        qte = request.POST.get('qte')
        id = request.POST.get('id')
        try:
            with transaction.atomic():
                panier = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
                if not panier.exists():
                    panier = Panier.objects.create(user=CompteUser.objects.get(user=request.user))
                    panier.nom_du_panier()
                    panier.save()
                else:
                    panier = panier.last()
                try:
                    qte = int(qte)
                    id = int(id)
                    produit = Produit.objects.get(id=id)
                    panierinter = panier.produits.filter(produits=produit, user=CompteUser.objects.get(user=request.user))
                except ValueError:
                    qte = 1
                except:
                    return Http404

                #initialisation
                if panierinter: #s'il y'a deja le produit dans le panier
                    panierinter = panierinter.first()
                    panier.prix -= panierinter.prix_du_produit
                    panier.quantite -= panierinter.quantite_du_produit
                    panier.save()
                    panierinter.quantite_du_produit += qte
                    panierinter.save()
                    panierinter.prix_du_produit = panierinter.quantite_du_produit * panierinter.produits.prix
                    panierinter.save()
                    panier.prix += panierinter.prix_du_produit
                    panier.quantite += panierinter.quantite_du_produit
                    panier.save()
                    messages.success(request, "Produit {} a été mise à jour dans le panier !".format(Produit.objects.get(id=id).nom))

                else:
                    panierinter = PanierItem.objects.create(produits=produit, user=CompteUser.objects.get(user=request.user))
                    panier.produits.add(panierinter)
                    panierinter.save()
                    panier.save()
                    panierinter.quantite_du_produit = qte
                    panierinter.save()
                    panierinter.prix_du_produit = panierinter.quantite_du_produit * panierinter.produits.prix
                    panierinter.save()
                    panier.prix += panierinter.prix_du_produit
                    panier.quantite += panierinter.quantite_du_produit
                    panier.save()
                    messages.success(request, "Produit ajouté au panier!")
        except IntegrityError:
            messages.warning(request, "Une erreur est apparue en interne. Merci de récommencer")
            return redirect('boutique:accueil')

    try:
        panierproduit = Panier.objects.get(user=CompteUser.objects.get(user=request.user), traite=False).produits.all()
    except MultipleObjectsReturned:
        panierproduit = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
        panierproduit = panierproduit.last().produits.all()
    except :
        panierproduit = []

    return render(request, 'boutique/panier.html', locals())

@login_required(login_url='boutique:connexion')
def sup_item_panier(request, pk):
    try:
        with transaction.atomic():

            try:
                id=int(pk)
                produit = Produit.objects.get(id=id)
                print(produit)
                paniersup = Panier.objects.filter(user=CompteUser.objects.get(user=request.user), traite=False)
            except ObjectDoesNotExist:
                messages.info(request, "Le produit n'existe plus dans le panier !")
                return redirect('boutique:accueil', permanent=True)
            except MultipleObjectsReturned:
                messages.info(request, "Le produit n'existe plus dans le panier !")
                return redirect('boutique:accueil', permanent=True)
            except:
                return Http404

            if paniersup.exists():
                paniersup = paniersup.last()
                try:
                    panierinter = paniersup.produits.filter(user=CompteUser.objects.get(user=request.user), produits=produit)
                    panierinter = panierinter.first()
                    paniersup.quantite -= panierinter.quantite_du_produit
                    paniersup.prix -= panierinter.prix_du_produit
                    paniersup.produits.remove(panierinter)
                    panierinter.delete()
                    paniersup.save()
                    messages.success(request, 'Le produit a été rétiré du panier !')
                except:
                    messages.info(request, "Le produit n'existe plus dans le panier !")
                    return redirect('boutique:accueil', permanent=True)
            else:
                return Http404
    except IntegrityError:
        messages.warning(request, "Une erreur est apparue en interne. Merci de récommencer")
        return redirect('boutique:accueil', permanent=True)

    return render(request, 'boutique/panier.html', locals())

# Achat du produit
def acheter(request, id_produit):
    if request.user.is_authenticated:
        try:
            with transaction.atomic():
                profil = CompteUser.objects.get(user=request.user)
                panier = Panier.objects.filter(user=profil, traite=False)
                if not panier.exists():
                    produit = get_object_or_404(Produit, id=id_produit)
                    quantite_produit = 1
                    prix_produit = quantite_produit * produit.prix
                else:
                    produit = get_object_or_404(Produit, id=id_produit)
                    panier= panier.last()
                    panierinter = panier.produits.filter(user=profil, produits=produit)
                    if panierinter:
                        panierinter = panierinter.last()
                        panier.prix -= panierinter.prix_du_produit
                        panier.quantite -= panierinter.quantite_du_produit
                        panier.save()
                        panierinter.quantite_du_produit += 1
                        panierinter.save()
                        panierinter.prix_du_produit = panierinter.quantite_du_produit * panierinter.produits.prix
                        panierinter.save()
                        panier.prix += panierinter.prix_du_produit
                        panier.quantite += panierinter.quantite_du_produit
                        panier.save()
                    else:
                        panierinter = PanierItem.objects.create(user=profil, produits=produit)
                        panierinter.save()
                        panier.produits.add(panierinter)
                        panier.save()
                        panierinter.quantite_du_produit = 1
                        panierinter.save()
                        panierinter.prix_du_produit = panierinter.quantite_du_produit * panierinter.produits.prix
                        panierinter.save()
                        panier.prix += panierinter.prix_du_produit
                        panier.quantite += panierinter.quantite_du_produit
                        panier.save()
                    prix_produit = panier.prix

        except IntegrityError:
            messages.warning(request, "Une erreur est apparue en interne. Merci de récommencer")
            return redirect('boutique:accueil', permanent=True)
    else:
        produit = get_object_or_404(Produit, id=id_produit)
        quantite_produit = 1
        prix_produit = quantite_produit * produit.prix

    formu = PayementForm(request.POST or None, error_class=ParagraphErrorList)
    envoi = False
    if formu.is_valid():
        nom = formu.cleaned_data['nom']
        prenom = formu.cleaned_data['prenom']
        email = formu.cleaned_data['email']
        adress = formu.cleaned_data['adress']
        telephone = formu.cleaned_data['telephone']
        newsletter = formu.cleaned_data['newsletter']
        method = request.POST.get('payement')
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
        if request.user.is_authenticated:
            if panier:
                panier.traite = True
                panier.save()
                commande = Commande.objects.create(contact=contact, panier=panier)
                commande.save()
            else:
                commande = Commande.objects.create(contact=contact, produit=produit, method=method)
                commande.save() 
        else:
            commande = Commande.objects.create(contact=contact, produit=produit, method=method)
            commande.save()

        if method == "L":
            return redirect('boutique:merci')
        else:
            return redirect("boutique:aurevoir")
    return render(request, 'boutique/achat.html', locals()) 

# Reglement à la caisse
@login_required(login_url='boutique:connexion')
def lacaisse(request):

    formu = PayementForm(request.POST or None)
    envoi = False
    if formu.is_valid():
        nom = formu.cleaned_data['nom']
        prenom = formu.cleaned_data['prenom']
        email = formu.cleaned_data['email']
        adress = formu.cleaned_data['adress']
        telephone = formu.cleaned_data['telephone']
        newsletter = formu.cleaned_data['newsletter']
        method = request.POST.get('payement')

        envoi = True #envoi de mail
        #enregistrement du contact
        try:
            with transaction.atomic():
                profil = CompteUser.objects.get(user=request.user)
                panier = Panier.objects.filter(user=profil, traite=False)
                panier = panier.last()
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
                commande = Commande.objects.create(contact=contact, panier=panier, method=method)
                commande.save()

                if method == "L":
                    return redirect('boutique:merci')
                else:
                    return redirect("boutique:aurevoir")
        except IntegrityError:
            messages.warning(request, "Une erreur est apparue en interne. Merci de récommencer")
            return redirect('boutique:accueil', permanent=True)

    return render(request, 'boutique/caisse.html', locals())

# Signaler un bug
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

# Prendre contact
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

   
    
