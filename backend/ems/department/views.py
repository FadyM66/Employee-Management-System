from rest_framework.decorators import api_view
from core.role_checker import role_required
from core.role_permitter import role_permitter
from core.validator import validator
from core.responses import Responses as r
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .serializer import department_serializer
from company.models import Company


@api_view(['POST'])
@role_required(['admin'])
@role_permitter
def create(request):
    """Create department endpoint"""

    try:
        new_record_data = request.data
        result = validator.validate_department_signup(new_record_data)
        model = request.model
        
        if isinstance(result, tuple):
            response, validated_data = result
            company = Company.objects.get(name=validated_data['company'])
            new_company = model(
                name=validated_data['name'],
                company=company
            )
            new_company.save()
            return response
        
        else:
            return result
        
    except ValidationError as e:
        print(f"Error: {str(e)}")
        return r.conflict

    except Exception as e :
        print(f'Error: {str(e)}')
        return r.server_error
    
    
@api_view(['GET'])
@role_required(['admin', 'manager'])
@role_permitter
def get(request):
    """Get department endpoint"""
    try:
        records = request.records
        serialized_records = department_serializer(records, many=True).data

        return r.set_data(serialized_records).ok

    except Exception as e :
        print(f'Error: {str(e)}')
        return r.server_error
    

@api_view(['DELETE'])
@role_required(['admin'])
@role_permitter
def delete(request):
    """Delete department endpoint"""

    try:

        if request.records:
            request.records.delete()
            return r.ok

        else:
            return r.not_found

    except Exception as e:
        return r.server_error


@api_view(['PATCH'])
@role_required(['admin'])
@role_permitter
def update(request):
    """Update department endpoint"""
    
    try:
        department_name = request.data['name']
        model = request.model
        department = model.objects.filter(name=department_name).first()
        
        if not department:
            return r.not_found
        
        new_record_data = request.data['new_data']
        result = validator.validator(new_record_data)
        
        if isinstance(result, dict):  
            for key, value in result.items():
                
                if key == 'company':
                    value = Company.objects.filter(name=value).first()
                    if not value:
                        return r.set_data({'errors': 'No company with the provided name.'}).invalid_data
                    
                setattr(department, key, value)  
                       
            department.save()
            return r.ok
        
        else:
            return r.invalid_data
            
    except IntegrityError as e:
        print(f"Error: {str(e)}")
        return r.conflict

    except Exception as e :
        print(f'Error: {str(e)}')
        return r.server_error