from rest_framework import serializers
from .models import Department


class department_serializer(serializers.ModelSerializer):
    number_of_employees = serializers.ReadOnlyField()
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Department
        fields = [
            'name', 
            'company_name',
            'number_of_employees'
        ]
