from .models import Profissional, Consultation
from rest_framework import serializers
from django.utils import timezone
import re

class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = '__all__'

    def validate_social_name(self, value):
        value = value.strip()  
        if not value:
            raise serializers.ValidationError("O nome social não pode estar vazio.")
        return value

    def validate_professional_register(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("O registro profissional não pode estar vazio.")
        
        if not value.replace('-', '').isalnum():
            raise serializers.ValidationError("Registro profissional deve conter apenas letras, números e hífen.")
        return value

    def validate_adress(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("O endereço não pode estar vazio.")
        return value

    def validate_phone_number(self, value):
        value = value.strip()
        cleaned = re.sub(r'[^0-9]', '', value)  
        if len(cleaned) < 10:
            raise serializers.ValidationError("Número de telefone inválido.")
        return cleaned

    

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'
    
    
    def validate_data(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("A data da consulta não pode ser no passado.")
        return value

    def validate(self, data):
        professional = data.get('professional')
        if professional and not professional.social_name:
            raise serializers.ValidationError("O profissional está inativo.")
        return data