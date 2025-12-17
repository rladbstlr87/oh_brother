from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ChurchViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'churches', ChurchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
