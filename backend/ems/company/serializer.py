from rest_framework import serializers
from .models import Company


class company_serializer(serializers.ModelSerializer):
    number_of_departments = serializers.ReadOnlyField()
    number_of_employees = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = [
            'id', 
            'name', 
            'number_of_departments', 
            'number_of_employees'
        ]
