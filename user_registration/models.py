from django.db import models

#Registering the principal benevolent member

class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=10)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    age = models.IntegerField()
    is_deceased = models.BooleanField(default=False)

    def __str__(self):
        return self.username

#Registering the spouse of the principal benevolent member

class Spouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spouses')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=10)
    age = models.IntegerField()
    is_deceased = models.BooleanField(default=False)

    def __str__(self):
        return self.name

#Registering the dependants of the principal benevolent member

class Dependant(models.Model):
    relationship_types = [
        ('son', 'son'),
        ('daughter', 'daughter'),
        ('father', 'father'),
        ('mother', 'mother'),
        ('father-in-law', 'father-in-law'),
        ('mother-in-law', 'mother-in-law'), 
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dependant')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    relationship = models.CharField(max_length=100, choices=relationship_types) #e.g son, daughter, etc
    age = models.IntegerField()
    is_deceased = models.BooleanField(default=False)

    def __str__(self):
        return self.name

#model for tracking payments and contributions

    
from django.db import models
from .utils import get_members_and_dependants

class Case(models.Model):
    case_number = models.CharField(max_length=20, unique=True)
    deceased_member_name = models.CharField(max_length=100)  # Name of the deceased member
    date_of_death = models.DateField()
    is_closed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cases')  # Link to the User model

    def save(self, *args, **kwargs):
        # Find and mark the deceased member
        deceased_member = None

        # Check in User, Spouse, and Dependant models
        deceased_member = User.objects.filter(name=self.deceased_member_name).first() or \
                          Spouse.objects.filter(name=self.deceased_member_name).first() or \
                          Dependant.objects.filter(name=self.deceased_member_name).first()

        if deceased_member:
            deceased_member.is_deceased = True
            deceased_member.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Case {self.case_number} - {self.deceased_member_name}"

class Payment(models.Model):
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, null=True, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    is_registration = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {'Registration' if self.is_registration else 'Contribution'}"

