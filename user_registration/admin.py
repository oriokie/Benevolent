from django.contrib import admin
from django.http import HttpResponse
from .forms import UserForm, SpouseForm, DependantForm, PaymentForm, CaseForm
import csv
from .models import User, Spouse, Dependant, Payment, Case
from .reporting import (
    generate_members_report,
    generate_members_and_dependants_report,
    generate_deceased_members_report,
    generate_case_contributions_report,
)

# Utility function for exporting data as CSV
def export_as_csv(queryset, filename):
    if not queryset:
        return HttpResponse("No data available to export.", content_type="text/plain")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    for record in queryset:
        writer.writerow(record.values())

    return response

def export_to_csv(queryset, filename, headers, data_accessor):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(headers)

    for obj in queryset:
        writer.writerow(data_accessor(obj))

    return response

@admin.action(description='Export Integrated List of Members with Spouses and Dependants')
def export_integrated_member_list(modeladmin, request, queryset):
    # Define the headers for your CSV file
    headers = ['Member Name', 'Member Phone', 'Spouse Name', 'Spouse Phone', 'Dependant Name', 'Dependant Phone', 'Dependant Relationship']

    def data_accessor(user):
        data = []
        spouses = user.spouses.all()
        dependants = user.dependant.all()
        max_len = max(len(spouses), len(dependants))

        for i in range(max_len):
            row = [user.name, user.phone_number]
            if i < len(spouses):
                spouse = spouses[i]
                row.extend([spouse.name, spouse.phone_number])
            else:
                row.extend(['', ''])

            if i < len(dependants):
                dependant = dependants[i]
                row.extend([dependant.name, dependant.phone_number, dependant.relationship])
            else:
                row.extend(['', '', ''])

            data.append(row)
        return data

    # Flatten the list of lists
    flattened_data = [item for sublist in queryset for item in data_accessor(sublist)]

    return export_to_csv(flattened_data, 'integrated_member_list.csv', headers, lambda x: x)


# Custom admin actions
@admin.action(description='Export Members Report')
def export_members_report(modeladmin, request, queryset):
    report = generate_members_report()
    return export_as_csv(report, 'members_report.csv')

@admin.action(description='Export Members and Dependants Report')
def export_members_and_dependants_report(modeladmin, request, queryset):
    report = generate_members_and_dependants_report()
    return export_as_csv(report, 'members_and_dependants_report.csv')

@admin.action(description='Export Deceased Members Report')
def export_deceased_members_report(modeladmin, request, queryset):
    report = generate_deceased_members_report(2023)  # Consider improving this
    return export_as_csv(report, 'deceased_members_report.csv')

@admin.action(description='Export Case Contributions Report')
def export_case_contributions_report(modeladmin, request, queryset):
    report = generate_case_contributions_report()
    return export_as_csv(report, 'case_contributions_report.csv')

@admin.action(description='Export Case Contribution Report')
def export_case_contribution_report(modeladmin, request, queryset):
    headers = ['Case Number', 'Member Name', 'Amount Contributed']

    def data_accessor(case):
        return [(case.case_number, payment.user.name, payment.amount) for payment in case.payments.all()]

    flattened_data = [item for case in queryset for item in data_accessor(case)]
    return export_to_csv(flattened_data, 'case_contribution_report.csv', headers, lambda x: x)


# Admin classes for each model
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('name', 'phone_number', 'email', 'is_deceased')
    actions = [export_members_report, export_deceased_members_report, export_integrated_member_list]

    def save_model(self, request, obj, form, change):
        # Ensure the password is set during user creation
        obj.set_password(obj.id_number)
        super().save_model(request, obj, form, change)

class SpouseAdmin(admin.ModelAdmin):
    form = SpouseForm
    list_display = ('name', 'phone_number', 'user', 'is_deceased')

class DependantAdmin(admin.ModelAdmin):
    form = DependantForm
    list_display = ('name', 'phone_number', 'user', 'relationship', 'is_deceased')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'case', 'amount', 'date', 'is_registration')
    form = PaymentForm

class CaseAdmin(admin.ModelAdmin):
    form = CaseForm
    list_display = ('case_number', 'deceased_member_name', 'date_of_death', 'is_closed')
    actions = [export_case_contributions_report]

# Register your models with their respective admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Spouse, SpouseAdmin)
admin.site.register(Dependant, DependantAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Case, CaseAdmin)
