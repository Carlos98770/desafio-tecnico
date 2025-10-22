from rest_framework.routers import DefaultRouter
from .views import ProfissionalViewSet, ConsultationViewSet

router = DefaultRouter()
router.register(r'profissionais', ProfissionalViewSet, basename='profissional')
router.register(r'consultations', ConsultationViewSet, basename='consultation')

urlpatterns = router.urls

#Caso haja uma necessidade de adicionar URLs adicionais, elas podem ser incluídas aqui.
# from django.urls import path, include
# urlpatterns += [
#     path(),
# ]
