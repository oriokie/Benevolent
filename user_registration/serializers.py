from rest_framework import serializers
from .models import User, Spouse, Dependant, Payment, Case

#These serializers handle conversion of model instances to JSON
#and vice versa

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spouse
        fields = '__all__'

class DependantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependant
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'