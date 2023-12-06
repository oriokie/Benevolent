from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, username, id_number, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(id_number)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, id_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, id_number, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    id_number = models.CharField(max_length=10)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    age = models.IntegerField(default=1)
    is_deceased = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id_number']

    objects = CustomUserManager()

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
