from api.views import DealsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('deals', DealsViewSet, basename='deals')

urlpatterns = [
    path('', include(router.urls)),
]