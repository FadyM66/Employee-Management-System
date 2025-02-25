from functools import wraps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from employee.models import Employee

def role_permitter(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        payload = request.payload
        role = payload.get('role')
        email = payload.get('email')
        method = request.method

        # Employee permissions
        if role == 'employee':
            if method not in ['GET', 'PATCH']:
                return JsonResponse(
                    {'error': 'Method not allowed for employees'}, 
                    status=405
                )

            try:
                employee = Employee.objects.get(email=email)
                
                if 'pk' in kwargs:
                    requested_employee = get_object_or_404(Employee, pk=kwargs['pk'])
                    if requested_employee != employee:
                        return JsonResponse(
                            {'error': 'Access to other records forbidden'}, 
                            status=403
                        )
                
                request.employee = employee

            except Employee.DoesNotExist:
                return JsonResponse(
                    {'error': 'Employee record not found'}, 
                    status=404
                )

        # Manager permissions
        elif role == 'manager':
            try:
                manager = Employee.objects.select_related('department').get(email=email)
                
                if not manager.department:
                    return JsonResponse(
                        {'error': 'Manager not assigned to a department'}, 
                        status=403
                    )

                if method == 'POST':
                    if str(request.data.get('department')) != str(manager.department.id):
                        return JsonResponse(
                            {'error': 'Can only create in your department'}, 
                            status=403
                        )
                
                elif method in ['GET', 'PATCH', 'DELETE'] and 'pk' in kwargs:
                    employee = get_object_or_404(Employee, pk=kwargs['pk'])
                    if employee.department != manager.department:
                        return JsonResponse(
                            {'error': 'Employee not in your department'}, 
                            status=403
                        )

                request.manager_department = manager.department

            except Employee.DoesNotExist:
                return JsonResponse(
                    {'error': 'Manager record not found'}, 
                    status=404
                )

        # Admin permissions - full access
        elif role == 'admin':
            pass

        else:
            return JsonResponse(
                {'error': 'Invalid user role'}, 
                status=403
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view