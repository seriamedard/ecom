from django.test import TestCase
from django.urls import reverse

# Create your tests here.

# Accueil page
    # la page doit retourner un code statut 200
class AccueilPageTestCase(TestCase):
    def test_accueil_page(self):
        reponse = self.client.get(reverse('boutique:accueil'))
        self.assertEqual(reponse.status_code, 200)
