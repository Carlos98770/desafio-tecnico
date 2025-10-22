from django.shortcuts import render
from .models import Profissional, Consultation
from .serializers import ProfissionalSerializer, ConsultationSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.

class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

#     Automaticamente fornece endpoints para:
        # GET /profissionais/ → list
        # POST /profissionais/ → create
        # GET /profissionais/<id>/ → retrieve
        # PUT/PATCH /profissionais/<id>/ → update
        # DELETE /profissionais/<id>/ → destroy

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    @action(detail=False, methods=['get'], url_path='profissional/(?P<professional_id>[^/.]+)')
    def por_profissional(self, request, professional_id=None):
        try:
            professional_id = int(professional_id)  # validação + sanitização
        except ValueError:
            return Response({"detail": "ID não inteiro."}, status=400)

        consultas = self.queryset.filter(professional__id=professional_id)
        serializer = ConsultationSerializer(consultas, many=True)
        return Response(serializer.data)