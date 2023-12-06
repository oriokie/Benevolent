from .models import User, Spouse, Dependant, Payment, Case
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from .models import Payment
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, ListView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django import forms


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

def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payment.html', {'payments': payments})

def case_list(request):
    cases = Case.objects.all()
    return render(request, 'case.html', {'cases': cases})


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    def form_valid(self, form):
        # Get the authenticated user
        authenticated_user = form.get_user()
        # Ensure the user is not None
        if authenticated_user is not None:
            # Set the success_url dynamically based on the user's pk (username in this case)
            success_url = reverse_lazy('member_detail', kwargs={'slug': authenticated_user.username})
            return HttpResponseRedirect(success_url)
        return super().form_invalid(form)

    def form_invalid(self, form):
        # This method is called when the form is invalid.
        # Check for user authentication and raise ValidationError only if not authenticated.
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = form.get_user  # Get the authenticated user if available

        if user is None or not user.check_password(password):
            raise forms.ValidationError('Invalid username or password')

        return super().form_invalid(form)


class MemberDetailView(DetailView):
    model = User
    template_name = 'member_detail.html'
    context_object_name = 'member'
    slug_field = 'username'

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['slug'])

@login_required
def member_detail(request, pk):
    # Retrieve the member using the primary key (pk)
    member = get_object_or_404(User, pk=pk)
    
    # You can customize this context dictionary with additional data
    context = {
        'member': member,
    }
    
    # Render the member detail template with the context data
    return render(request, 'member_detail.html', context)


@login_required
def spouse_detail(request, pk):
    # Retrieve the spouse using the primary key (pk)
    spouse = get_object_or_404(Spouse, pk=pk)
    
    # You can customize this context dictionary with additional data
    context = {
        'spouse': spouse,
    }
    
    # Render the spouse detail template with the context data
    return render(request, 'spouse_detail.html', context)

@login_required
def dependant_list(request):
    # Retrieve the list of dependants
    dependants = Dependant.objects.all()
    
    # You can customize this context dictionary with additional data
    context = {
        'dependants': dependants,
    }
    
    # Render the dependant list template with the context data
    return render(request, 'dependant_list.html', context)

