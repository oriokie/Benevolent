from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SpouseViewSet, DependantViewSet, PaymentViewSet, CaseViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'spouses', SpouseViewSet)
router.register(r'dependants', DependantViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'cases', CaseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # You can add more URL patterns here
]
