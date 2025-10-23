from rest_framework.test import APITestCase
from api.models import Profissional

class ProfissionalModelTest(APITestCase):

    

    def test_profissional_creation(self):
        prof = Profissional.objects.create(
            social_name = "Dr. Bacteria",
            professional_register = "Cardiologista",
            adress = "ECT-UFRN 2022",
            phone_number = "1234567890"
        )

        self.assertIsInstance(prof, Profissional)
        self.assertEqual(Profissional.objects.count(),1)
        self.assertEqual(prof.social_name, prof.social_name)
        self.assertEqual(prof.professional_register, prof.professional_register)
        self.assertEqual(prof.adress, prof.adress)
        self.assertEqual(prof.phone_number, prof.phone_number)

    def test_profissional_read(self):
        prof = Profissional.objects.create(
            social_name = "Dr. Bacteria",
            professional_register = "Cardiologista",
            adress = "ECT-UFRN 2022",
            phone_number = "1234567890"
        )

        profissional_db = Profissional.objects.get(id=prof.id)
        self.assertIsNotNone(profissional_db)
        self.assertEqual(profissional_db.social_name, prof.social_name)
        self.assertEqual(profissional_db.professional_register, prof.professional_register)
        self.assertEqual(profissional_db.adress, prof.adress)
        self.assertEqual(profissional_db.phone_number, prof.phone_number)
        
    def test_profissional_update(self):
        prof = Profissional.objects.create(
            social_name = "Dr. Bacteria",
            professional_register = "Cardiologista",
            adress = "ECT-UFRN 2022",
            phone_number = "1234567890"
        )
        
        profissional = Profissional.objects.get(id=prof.id)
        profissional.social_name = "Zé da manga"
        profissional.professional_register = "Neurologista"
        profissional.adress = "UFRN - DCA"
        profissional.phone_number = "9876543210"
        profissional.save()
        profissional.refresh_from_db()
        self.assertEqual(profissional.social_name, "Zé da manga")

    def test_profissional_delete(self):
        prof = Profissional.objects.create(
            social_name = "Dr. Bacteria",
            professional_register = "Cardiologista",
            adress = "ECT-UFRN 2022",
            phone_number = "1234567890"
        )
        profissional = Profissional.objects.get(id=prof.id)
        profissional.delete()
        self.assertEqual(Profissional.objects.filter(id=prof.id).count(), 0)
        

