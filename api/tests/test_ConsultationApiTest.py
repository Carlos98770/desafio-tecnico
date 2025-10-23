from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from api.models import Profissional, Consultation
from django.conf import settings

class ConsultationApiTest(APITestCase):

    def setUp(self):
        self.prof = Profissional.objects.create(
            social_name = "Dr. Bacteria",
            professional_register = "Cardiologista",
            adress = "ECT-UFRN 2022",
            phone_number = "1234567890"
        )
        self.consulta = Consultation.objects.create(
            data=timezone.now() + timedelta(days=1),
            professional=self.prof
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Api-Key {settings.API_KEY}')

    def test_list_consultations(self):
        url = reverse('consultation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_consultation(self):
        url = reverse('consultation-list')
        data = {
            "data": (timezone.now() + timedelta(days=3)).isoformat(),
            "professional": self.prof.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consultation.objects.count(), 2)

    def test_retrieve_consultation(self):
        url = reverse('consultation-detail', args=[self.consulta.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['professional'], self.prof.id)

    def test_update_consultation(self):
        url = reverse('consultation-detail', args=[self.consulta.id])
        nova_data = timezone.now() + timedelta(days=5)
        data = {"data": nova_data.isoformat()}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.consulta.refresh_from_db()
        self.assertEqual(self.consulta.data, nova_data)

    def test_delete_consultation(self):
        url = reverse('consultation-detail', args=[self.consulta.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Consultation.objects.filter(id=self.consulta.id).exists())

    def test_filter_by_professional_id(self):
        url = reverse('consultation-por-profissional', kwargs={'professional_id': self.prof.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['professional'], self.prof.id)
