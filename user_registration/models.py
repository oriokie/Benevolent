from django.db import models

#Registering the principal benevolent member

class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=10)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    age = models.IntegerField()

    def __str__(self):
        return self.username

#Registering the spouse of the principal benevolent member

class Spouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spouse')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    id_number = models.CharField(max_length=10)
    age = models.IntegerField()

    def __str__(self):
        return self.username

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

    def __str__(self):
        return self.username

#model for tracking payments and contributions

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    is_registration = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {'Registration' if self.is_registration else 'Contribution'}"
    

#model for tracking Cases
class Case(models.Model):
    deceased = models.CharField(max_length=100)  # Name of the deceased person
    relationship_with_user = models.CharField(max_length=50)  # Relation to the user
    date_of_death = models.DateField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Case of {self.deceased}"

