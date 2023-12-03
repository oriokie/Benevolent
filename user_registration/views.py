from django.shortcuts import render
from django.shortcuts import render
from .models import User, Spouse, Dependant, Payment, Case
from django.shortcuts import render, redirect
from .forms import UserForm

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Spouse, Dependant, Payment, Case
from .serializers import UserSerializer, SpouseSerializer, DependantSerializer, PaymentSerializer, CaseSerializer
from rest_framework.decorators import action

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
    @action(detail=True, methods=['post'])
    def report_death(self, request, pk=None):
        case = self.get_object()
        # Add logic to mark the case as reported and trigger contributions
        for user in User.objects.filter(is_active=True):
            Payment.objects.create(
                user=user,
                amount=500.00,  # Contribution amount
                is_registration=False
            )
        return Response({'status': 'Contributions recorded'})


def user_list(request):
    users = User.objects.all()
    return render(request, 'user.html', {'users': users})

def spouse_list(request):
    spouses = Spouse.objects.all()
    return render(request, 'spouse.html', {'spouses': spouses})

def dependant_list(request):
    dependants = Dependant.objects.all()
    return render(request, 'dependant.html', {'dependants': dependants})

def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payment.html', {'payments': payments})

def case_list(request):
    cases = Case.objects.all()
    return render(request, 'case.html', {'cases': cases})


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to the user list page after saving
    else:
        form = UserForm()

    return render(request, 'add_user.html', {'form': form})

