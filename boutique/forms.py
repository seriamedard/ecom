from django import forms
from django.forms.utils import ErrorList
from django.http import HttpRequest
from django.contrib.auth.models import User
from .models import CompteUser
class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist" style="color:#f9ac68;" >%s</div>'%''.join(['<p class="error">%s</p>' % e for e in self])

class CompteUserForm(forms.Form):
    username = forms.CharField(max_length=255, label="Nom d'utilisateur",
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder': "nom d'utilisateur",
                                    'aria-describedby':"'basic-addon2'",
                                    'autofocus':'autofocus',
                                }))

    first_name = forms.CharField(max_length=100, label='Nom',required=True,
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder': "Votre nom",
                                    'aria-describedby':"'basic-addon2'",
                                }))
    last_name = forms.CharField(max_length=100, label='Prénom', 
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder': "Votre prénom",
                                    'aria-describedby':"basic-addon2",
                                }))

    email = forms.EmailField(required=True,
                            widget=forms.EmailInput(attrs={
                            'class':'form-control',
                            'placeholder': "Ex: jeanbello@gmail.com",
                            'aria-describedby':"emailHelp",
                            }))

    password = forms.CharField(min_length=6,
                                max_length=255,
                                required=True,
                                label='Mot de passe',
                                widget=forms.PasswordInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'Mot de passe',
                                    'aria-describedby':"passwordlHelp",
                                }))

    def clean_username(self): 
        username = self.cleaned_data['username']

        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        if u.DoesNotExist:
            raise forms.ValidationError("Le nom d'utilisateur {} est déja utilisé!".format(username))
        return username


class ProfilForm(forms.Form):
    username = forms.CharField(max_length=255, 
                                label="Nom d'utilisateur",
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder': "nom d'utilisateur",
                                    'aria-describedby':"'basic-addon2'",
                                    'autofocus':'autofocus',
                                    'value':"",
                                }))

    first_name = forms.CharField(max_length=100, label='Nom',required=True,
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder': "Votre nom",
                                    'aria-describedby':"'basic-addon2'",
                                }))
    last_name = forms.CharField(max_length=100, label='Prénom', 
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder': "Votre prénom",
                                    'aria-describedby':"basic-addon2",
                                }))

    email = forms.EmailField(required=True,
                            widget=forms.EmailInput(attrs={
                            'class':'form-control',
                            'placeholder': "Ex: jeanbello@gmail.com",
                            'aria-describedby':"emailHelp",
                            }))
    
    bio = forms.CharField(label='Bio', required=False, widget=forms.Textarea(attrs={
                            'class':'form-control',
                            'placeholder': 'brève biographie de vous',
                        }))
    newsletter = forms.BooleanField(label='Newsletter',
                                    required=False,
                                    widget=forms.CheckboxInput(attrs={
                                    }))

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur",
                                max_length=255,
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder':"Nom d'utisateur",
                                }))
    password = forms.CharField(label="Mot de passe",widget=forms.PasswordInput(attrs={
                                'class':'form-control',
                                'placeholder':'Mot de passe ici',
                                }))


class PasswordChangeForm(forms.Form):
    oldpassword = forms.CharField(label='Ancien mot de passe', widget=forms.PasswordInput(attrs={
                                'class':'form-control',
                                'placeholder': 'Votre ancien mot de passe',
                                }))
    newpassword = forms.CharField(label='Nouveau mot de passe', min_length=6, widget=forms.PasswordInput(attrs={
                                'class': 'form-control',
                                'placeholder':'Votre nouveau mot de passe',
                                }))
    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        oldpassword = cleaned_data.get('oldpassword')
        newpassword = cleaned_data.get('newpassword')
        if oldpassword and newpassword:
            if oldpassword == newpassword:
                self.add_error('newpassword', "Votre nouveau mot de passe doit être différent de l'ancien.")
        return cleaned_data


class NewsletterForm(forms.Form):
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder':'Prénom',
                                }))
    email = forms.EmailField(required=True,
                            widget=forms.EmailInput(attrs={
                            'class':'form-control',
                            'placeholder': "Votre mail",
                            'aria-describedby':"emailHelp",
                            }))


class BugForm(forms.Form):
    description = forms.CharField(label='Description du bug',
                                required=True,
                                widget=forms.Textarea(attrs={
                                    'class':'form-control',
                                    'placeholder':'Exemple:\n1. Se connecter sur le site? \n-->Avec un compte username....\
                                        \n2.Ajouter un produit au panier?\n--> Un produit ne se met pas à jour....\
                                        \n.\n.\n.',
                                }))


class ContactUsForm(forms.Form):
    prenom = forms.CharField(label="Prénom",
                            widget=forms.TextInput(attrs={
                                'class':'form-control',
                                'placeholder':'Prénom',
                            }))
    email = forms.EmailField(label="Email Adress",
                            widget=forms.EmailInput(attrs={
                                'class':'form-control',
                                'placeholder': "Votre mail",
                                'aria-describedby':"emailHelp",
                            }))
    demande = forms.CharField(label="Posez votre demande",
                            widget=forms.Textarea(attrs={
                                'class':'form-control',
                                'placeholder':"formulez votre demande",
                            })) 
    newsletter = forms.BooleanField(label="Newsletter",
                                    required=False,
                                    widget=forms.CheckboxInput(attrs={
                                    }))


class PayementForm(forms.Form):
    nom = forms.CharField(max_length=100,
                        widget=forms.TextInput(attrs={
                            'class':'form-control',
                            'placeholder':'Nom',
                        }))

    prenom = forms.CharField(max_length=100,
                                required=False,
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'Prénom',
                                }))

    email = forms.EmailField(required=True,
                                widget=forms.EmailInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'Email',
                                }))
                            
    adress = forms.CharField(widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'Adresse de livraison',
                                }))
    telephone = forms.CharField(widget=forms.NumberInput(attrs={
                                'class':'form-control',
                                'type':'tel',
                                'placeholder':'Telephone',
                                }))
    newsletter = forms.BooleanField(label='Newsletter',
                                required=False,
                                widget=forms.CheckboxInput(attrs={
                                }))
