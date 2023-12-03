from django.db.models import Q
from .models import User, Spouse, Dependant
def get_members_and_dependants():
    members_and_dependants = []

    # Query all users and their cases, ensuring they are not deceased
    users_with_cases = User.objects.prefetch_related('cases').filter(is_deceased=False)

    for user in users_with_cases:
        user_info = {
            'name': user.name,
            'phone_number': user.phone_number,
            'id_number': user.id_number,
            'username': user.username,
            'email': user.email,
            'age': user.age,
            'is_deceased': user.is_deceased
        }
        members_and_dependants.append(user_info)

        # Query spouses and dependants for the current user, ensuring they are not deceased
        for spouse in user.spouses.filter(is_deceased=False):
            spouse_info = {
                'name': spouse.name,
                'phone_number': spouse.phone_number,
                'id_number': spouse.id_number,
                'age': spouse.age,
                'is_deceased': spouse.is_deceased
            }
            members_and_dependants.append(spouse_info)

        for dependant in user.dependant.filter(is_deceased=False):
            dependant_info = {
                'name': dependant.name,
                'phone_number': dependant.phone_number,
                'relationship': dependant.relationship,
                'age': dependant.age,
                'is_deceased': dependant.is_deceased
            }
            members_and_dependants.append(dependant_info)

    return members_and_dependants
