from django.test import TestCase
from .models import User, Spouse, Dependant
from .utils import get_members_and_dependants

class MembersAndDependantsTest(TestCase):
    def setUp(self):
        # Set up test data with all fields
        self.user1 = User.objects.create(
            name='User 1',
            phone_number='1234567890',
            id_number='ID123',
            username='user1',
            email='user1@example.com',
            age=30,
            is_deceased=False
        )
        self.spouse1 = Spouse.objects.create(
            user=self.user1,
            name='Spouse 1',
            phone_number='0987654321',
            id_number='ID124',
            age=28,
            is_deceased=False
        )
        self.dependant1 = Dependant.objects.create(
            user=self.user1,
            name='Dependant 1',
            phone_number='1231231234',
            relationship='son',
            age=5,
            is_deceased=False
        )

    def test_get_members_and_dependants(self):
        expected_result = [
            {
                'name': self.user1.name,
                'phone_number': self.user1.phone_number,
                'id_number': self.user1.id_number,
                'username': self.user1.username,
                'email': self.user1.email,
                'age': self.user1.age,
                'is_deceased': self.user1.is_deceased
            },
            {
                'name': self.spouse1.name,
                'phone_number': self.spouse1.phone_number,
                'id_number': self.spouse1.id_number,
                'age': self.spouse1.age,
                'is_deceased': self.spouse1.is_deceased
            },
            {
                'name': self.dependant1.name,
                'phone_number': self.dependant1.phone_number,
                'relationship': self.dependant1.relationship,
                'age': self.dependant1.age,
                'is_deceased': self.dependant1.is_deceased
            }
        ]

        actual_result = get_members_and_dependants()
        self.assertEqual(actual_result, expected_result)

# Run this test using Django's test runner
