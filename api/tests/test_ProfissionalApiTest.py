from rest_framework.test import APITestCase
from api.models import Profissional
from django.urls import reverse
from django.conf import settings
from rest_framework import status

class ProfissionalApiTest(APITestCase):  

    def setUp(self):
        self.prof = Profissional.objects.create(
            social_name = "Dr. Bacteria",
            professional_register = "Cardiologista",
            adress = "ECT-UFRN 2022",
            phone_number = "1234567890"
        )
        self.list_url = reverse('profissional-list')

        self.client.credentials(HTTP_AUTHORIZATION=f'Api-Key {settings.API_KEY}')

    def test_list_profissionais(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_profissional(self):
        data = {
            "social_name": "Zé da Manga",
            "professional_register": "Neurologista",
            "adress": "UFRN - DCA",
            "phone_number": "9876543210"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profissional.objects.count(), 2)  # já existia 1 no setUp
        self.assertEqual(Profissional.objects.last().social_name, "Zé da Manga")

    def test_retrieve_profissional(self):
        url = reverse('profissional-detail', args=[self.prof.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['social_name'], self.prof.social_name)

    def test_update_profissional(self):
        url = reverse('profissional-detail', args=[self.prof.id])
        data = {
            "social_name": "Atualizado"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.prof.refresh_from_db()
        self.assertEqual(self.prof.social_name, "Atualizado")

    def test_delete_profissional(self):
        url = reverse('profissional-detail', args=[self.prof.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profissional.objects.filter(id=self.prof.id).exists())