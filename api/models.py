from django.db import models

# Create your models here.
class Profissional(models.Model):
    social_name = models.CharField(max_length=100)
    professional_register = models.CharField(max_length=50, unique=True)
    adress = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.social_name
    
class Consultation(models.Model):
    
    data = models.DateTimeField()
    professional = models.ForeignKey(Profissional, on_delete=models.CASCADE)