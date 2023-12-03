from .models import User, Case
from django.utils import timezone
from django.db.models import Sum


def generate_members_report():
    members = User.objects.all().values(
        'name', 'phone_number', 'id_number', 'username', 'email', 'age', 'is_deceased'
    )
    # Additional processing to format the report (e.g., create a CSV file)
    return members

def generate_members_and_dependants_report():
    members = User.objects.prefetch_related('dependant').values(
        'name', 'dependant__name', 'dependant__phone_number', 'dependant__relationship', 'dependant__age', 'dependant__is_deceased'
    )
    # Format the report
    return members

def generate_deceased_members_report(year):
    start_date = timezone.datetime(year, 1, 1)
    end_date = timezone.datetime(year, 12, 31)
    deceased_members = User.objects.filter(
        is_deceased=True, 
        deceased_date__range=(start_date, end_date)
    ).values('name', 'date_of_death')
    # Format the report
    return deceased_members


def generate_case_contributions_report():
    case_contributions = Case.objects.annotate(
        total_contributions=Sum('payment__amount')
    ).values('case_number', 'total_contributions')
    # Format the report
    return case_contributions
