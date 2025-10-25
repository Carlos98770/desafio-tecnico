from rest_framework.routers import DefaultRouter
from .views import ProfissionalViewSet, ConsultasViewSet

router = DefaultRouter()
router.register(r'profissionais', ProfissionalViewSet, basename='profissional')
router.register(r'consultas', ConsultasViewSet, basename='Consultas')

urlpatterns = router.urls

#Caso haja uma necessidade de adicionar URLs adicionais, elas podem ser incluídas aqui.
# from django.urls import path, include
# urlpatterns += [
#     path(),
# ]
