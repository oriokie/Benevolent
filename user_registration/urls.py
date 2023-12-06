from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SpouseViewSet, DependantViewSet, PaymentViewSet, CaseViewSet, CustomLoginView, MemberDetailView
from .import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'spouses', SpouseViewSet)
router.register(r'dependants', DependantViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'cases', CaseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('users/', views.user_list, name='user_list'),
    path('spouses/', views.spouse_list, name='spouse_list'),
    path('dependants/', views.dependant_list, name='dependant_list'),
    path('payments/', views.payment_list, name='payment_list'),
    path('cases/', views.case_list, name='case_list'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('member_detail/<slug:slug>/', MemberDetailView.as_view(), name='member_detail'),
    path('spouse/<int:pk>/', views.spouse_detail, name='spouse_detail'),
    path('dependant/', views.dependant_list, name='dependant_list'),
]
