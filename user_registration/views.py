from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Spouse, Dependant, Payment, Case
from .serializers import UserSerializer, SpouseSerializer, DependantSerializer, PaymentSerializer, CaseSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        # Create initial payment record
        Payment.objects.create(
            user=user,
            amount=500.00,  # Registration amount
            is_registration=True
        )
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

class SpouseViewSet(viewsets.ModelViewSet):
    queryset = Spouse.objects.all()
    serializer_class = SpouseSerializer

class DependantViewSet(viewsets.ModelViewSet):
    queryset = Dependant.objects.all()
    serializer_class = DependantSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

