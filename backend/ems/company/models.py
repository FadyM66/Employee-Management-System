from django.db import models
from django.core.validators import MinLengthValidator
from employee.models import Employee


class Company(models.Model):

    name = models.CharField(
        max_length=255, 
        unique=True,
    )

    def __str__(self):
        return self.name

    @property
    def number_of_departments(self):
        return self.departments.count()
    
    @property
    def number_of_employees(self):
        return Employee.objects.filter(department__company=self).count()
