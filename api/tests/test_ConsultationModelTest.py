from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from api.models import Consultation, Profissional

class ConsultationModelTest(APITestCase):

    def setUp(self):
        self.prof = Profissional.objects.create(
            social_name="Dr. Bacteria",
            professional_register="12345",
            adress="Rua das Flores, 123",
            phone_number="1234567890"
        )

    def test_consultation_creation(self):
        consulta = Consultation.objects.create(
            data=timezone.now() + timedelta(days=1),  # data futura
            professional=self.prof
        )
        self.assertIsInstance(consulta, Consultation)
        self.assertEqual(Consultation.objects.count(), 1)
        self.assertEqual(consulta.professional, self.prof)

    def test_consultation_read(self):
        consulta = Consultation.objects.create(
            data=timezone.now() + timedelta(days=1),
            professional=self.prof
        )
      
        consulta_db = Consultation.objects.get(id=consulta.id)
        self.assertIsNotNone(consulta_db)
        self.assertEqual(consulta_db.data, consulta.data)
        self.assertEqual(consulta_db.professional.id, self.prof.id)

    def test_consultation_update(self):
        consulta = Consultation.objects.create(
            data=timezone.now() + timedelta(days=1),
            professional=self.prof
        )
        nova_data = timezone.now() + timedelta(days=5)
        consulta.data = nova_data
        consulta.save()
        consulta.refresh_from_db()  
        self.assertEqual(consulta.data, nova_data)

    def test_consultation_delete(self):
        consulta = Consultation.objects.create(
            data=timezone.now() + timedelta(days=1),
            professional=self.prof
        )
        consulta_id = consulta.id
        consulta.delete()
        self.assertEqual(Consultation.objects.filter(id=consulta_id).count(), 0)
