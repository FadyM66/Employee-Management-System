from functools import wraps

from company.models import Company
from department.models import Department
from employee.models import Employee
from user.models import User

from .validator import validator
from .responses import Responses as r
from django.core.exceptions import ValidationError
from django.db import IntegrityError


def role_permitter(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:

            # Extract authentication information from request
            payload = request.payload

            role = payload.get("role")
            email = payload.get("email")

            method = request.method

            data = request.data

            # Determine which model to use based on the view function's module
            models = {
                "company": Company,
                "department": Department,
                "employee": Employee,
                "user": User,
            }

            module_name = view_func.__module__
            app_name = module_name.split(".")[0]
            model = models.get(app_name)

            # Admin has full access to all operations
            if role == "admin":

                if method == "GET":
                    
                    is_valid = validator.validator(data)

                    if isinstance(is_valid, dict):

                        if app_name == 'department' and len(is_valid.items()) > 0:

                            is_valid['company__name'] = is_valid['company']
                            del is_valid['company']

                        request.records = model.objects.filter(**is_valid)
                        
                        if request.records.count() == 0:
                            return r.not_found
                    else:
                        return is_valid

                elif method == "POST":
                    request.model = model
                    
                elif method == "DELETE":
                    data = validator.validator(data)
                    
                    if isinstance(data, dict):
                        if app_name == 'department':
                            data['company__name'] = data['company']
                            del data['company']

                        request.records = model.objects.filter(**data)
                        if request.records.count() == 0:
                            return r.not_found
                    else:
                        return r.invalid_data

                elif method == "PATCH":
                    request.model = model

                else:
                    return r.method_not_allowed

                return view_func(request, *args, **kwargs)

            # Manager has access to his department members whether users or employees
            # Manager cannot change the company or the department of an employee
            # Manager cannot set a user's role into admin or manager, just employee
            elif role == "manager":

                try:
                    manager = Employee.objects.get(email=email)
                except Employee.DoesNotExist:
                    return r.forbidden

                if method == "GET":
                    if model == Company:
                        request.records = model.objects.filter(
                            name=manager.department.company
                        )
                        if request.records.count() == 0:
                            return r.not_found

                    elif model == Department:
                        request.records = model.objects.filter(name=manager.department)
                        if request.records.count() == 0:
                            return r.not_found
                        
                    elif model == Employee:
                        request.records = model.objects.filter(
                            department=manager.department
                        )

                    elif model == User:
                        request.records = Employee.objects.filter(
                            department=manager.department
                        ).values_list("email", flat=True)

                    else:
                        return r.forbidden

                    return view_func(request, *args, **kwargs)

                elif method in ["POST", "PATCH"]:
                    if model in ["employee", "user"]:

                        if "role" in data and data.role != "employee":
                            return r.forbidden

                        if (
                            data.department
                            and data.department == manager.department
                            and data.company
                            and data.company == manager.company
                        ):
                            request.model = model

                        elif data.email in Employee.objects.filter(
                            department=manager.department
                        ).values_list("email", flat=True):
                            request.model = model

                        else:
                            return r.forbidden

                        return view_func(request, *args, **kwargs)

                elif method == "DELETE":
                    if data.email and data.email in Employee.objects.filter(
                        department=manager.department
                    ).values_list("email", flat=True):
                        request.records = model.objects.get(email=data.email)
                        return view_func(request, *args, **kwargs)

                    return r.forbidden

                else:
                    return r.method_not_allowed

            elif role == "employee":
                if method == "GET":
                    if model == Employee:
                        request.records = Employee.objects.get(email=email)

                    elif model == User:
                        request.records = User.objects.get(email=email)

                    return view_func(request, *args, **kwargs)

                elif method == "PATCH":
                    request.model = model

                    return view_func(request, *args, **kwargs)

        except model.DoesNotExist:
            return r.not_found

        except ValidationError:
            return r.invalid_data

        except IntegrityError:
            return r.conflict

        except KeyError:
            return r.invalid_data

        except AttributeError:
            return r.invalid_data

        except Exception as e:
            print(f"Error: {e}")
            return r.server_error

    return _wrapped_view
