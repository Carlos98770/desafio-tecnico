from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from api.models import Consultas, Profissional

class ConsultasModelTest(APITestCase):

    def setUp(self):
        self.prof = Profissional.objects.create(
            social_name="Dr. Bacteria",
            professional_register="12345",
            adress="Rua das Flores, 123",
            phone_number="1234567890"
        )

    def test_Consultas_creation(self):
        consulta = Consultas.objects.create(
            data=timezone.now() + timedelta(days=1),  # data futura
            professional=self.prof
        )
        self.assertIsInstance(consulta, Consultas)
        self.assertEqual(Consultas.objects.count(), 1)
        self.assertEqual(consulta.professional, self.prof)

    def test_Consultas_read(self):
        consulta = Consultas.objects.create(
            data=timezone.now() + timedelta(days=1),
            professional=self.prof
        )
      
        consulta_db = Consultas.objects.get(id=consulta.id)
        self.assertIsNotNone(consulta_db)
        self.assertEqual(consulta_db.data, consulta.data)
        self.assertEqual(consulta_db.professional.id, self.prof.id)

    def test_Consultas_update(self):
        consulta = Consultas.objects.create(
            data=timezone.now() + timedelta(days=1),
            professional=self.prof
        )
        nova_data = timezone.now() + timedelta(days=5)
        consulta.data = nova_data
        consulta.save()
        consulta.refresh_from_db()  
        self.assertEqual(consulta.data, nova_data)

    def test_Consultas_delete(self):
        consulta = Consultas.objects.create(
            data=timezone.now() + timedelta(days=1),
            professional=self.prof
        )
        consulta_id = consulta.id
        consulta.delete()
        self.assertEqual(Consultas.objects.filter(id=consulta_id).count(), 0)
